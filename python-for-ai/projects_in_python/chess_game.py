"""
Realistic Chess Game — pure Python (engine + pygame GUI in one file).

Rules implemented:
  - All piece movement rules (pawn, knight, bishop, rook, queen, king)
  - Check, checkmate, stalemate detection
  - Castling (kingside & queenside), including the "can't castle through/out of check" rule
  - En passant capture
  - Pawn promotion (choose queen/rook/bishop/knight via on-screen menu)
  - Fifty-move rule and threefold repetition draw detection
  - Turn enforcement, legal-move highlighting, move log, undo (press U)

Run locally with:  pip install pygame   then   python chess_game.py
"""

import sys
import copy

# ============================================================
#  CHESS ENGINE  (no pygame dependency — fully unit-testable)
# ============================================================

WHITE, BLACK = 'w', 'b'


def other(color):
    return BLACK if color == WHITE else WHITE


class Move:
    """A fully-specified move, storing everything needed to undo it."""

    __slots__ = (
        'sr', 'sc', 'er', 'ec', 'piece', 'captured',
        'is_en_passant', 'is_castle', 'promotion',
        'prev_castling_rights', 'prev_ep_target', 'prev_halfmove_clock',
    )

    def __init__(self, sr, sc, er, ec, piece, captured,
                 is_en_passant=False, is_castle=False, promotion=None):
        self.sr, self.sc, self.er, self.ec = sr, sc, er, ec
        self.piece = piece
        self.captured = captured
        self.is_en_passant = is_en_passant
        self.is_castle = is_castle
        self.promotion = promotion
        # filled in by make_move() for undo purposes
        self.prev_castling_rights = None
        self.prev_ep_target = None
        self.prev_halfmove_clock = None

    def uci(self):
        files = 'abcdefgh'
        s = f"{files[self.sc]}{8 - self.sr}{files[self.ec]}{8 - self.er}"
        if self.promotion:
            s += self.promotion[1]
        return s


class ChessEngine:
    def __init__(self):
        self.board = self._starting_board()
        self.turn = WHITE
        # castling rights: king-side / queen-side for each color
        self.castling = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.ep_target = None  # (row, col) square a pawn can capture en-passant into
        self.halfmove_clock = 0  # for the 50-move rule
        self.move_log = []
        self.position_counts = {}
        self._record_position()

    # ---------------------------------------------------------------
    # Board setup
    # ---------------------------------------------------------------
    @staticmethod
    def _starting_board():
        b = [[None] * 8 for _ in range(8)]
        back = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        for c in range(8):
            b[0][c] = BLACK + back[c]
            b[1][c] = BLACK + 'p'
            b[6][c] = WHITE + 'p'
            b[7][c] = WHITE + back[c]
        return b

    def piece_at(self, r, c):
        return self.board[r][c]

    @staticmethod
    def in_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def king_square(self, color):
        target = color + 'k'
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == target:
                    return (r, c)
        return None  # should never happen in a legal game

    # ---------------------------------------------------------------
    # Attack detection (used for check + castling legality)
    # ---------------------------------------------------------------
    def squares_attacked_by(self, color):
        """Return the set of squares attacked by `color`, ignoring pins/checks."""
        attacked = set()
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is None or p[0] != color:
                    continue
                kind = p[1]
                if kind == 'p':
                    d = -1 if color == WHITE else 1
                    for dc in (-1, 1):
                        rr, cc = r + d, c + dc
                        if self.in_bounds(rr, cc):
                            attacked.add((rr, cc))
                elif kind == 'n':
                    for dr, dc in ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                                   (1, -2), (1, 2), (2, -1), (2, 1)):
                        rr, cc = r + dr, c + dc
                        if self.in_bounds(rr, cc):
                            attacked.add((rr, cc))
                elif kind == 'k':
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            if dr == 0 and dc == 0:
                                continue
                            rr, cc = r + dr, c + dc
                            if self.in_bounds(rr, cc):
                                attacked.add((rr, cc))
                else:
                    dirs = []
                    if kind in ('r', 'q'):
                        dirs += [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if kind in ('b', 'q'):
                        dirs += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    for dr, dc in dirs:
                        rr, cc = r + dr, c + dc
                        while self.in_bounds(rr, cc):
                            attacked.add((rr, cc))
                            if self.board[rr][cc] is not None:
                                break
                            rr += dr
                            cc += dc
        return attacked

    def in_check(self, color):
        ksq = self.king_square(color)
        if ksq is None:
            return False
        return ksq in self.squares_attacked_by(other(color))

    # ---------------------------------------------------------------
    # Pseudo-legal move generation
    # ---------------------------------------------------------------
    def _pseudo_legal_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is None or p[0] != color:
                    continue
                kind = p[1]
                if kind == 'p':
                    moves += self._pawn_moves(r, c, color)
                elif kind == 'n':
                    moves += self._knight_moves(r, c, color)
                elif kind == 'b':
                    moves += self._sliding_moves(r, c, color, [(-1, -1), (-1, 1), (1, -1), (1, 1)])
                elif kind == 'r':
                    moves += self._sliding_moves(r, c, color, [(-1, 0), (1, 0), (0, -1), (0, 1)])
                elif kind == 'q':
                    moves += self._sliding_moves(r, c, color,
                                                   [(-1, 0), (1, 0), (0, -1), (0, 1),
                                                    (-1, -1), (-1, 1), (1, -1), (1, 1)])
                elif kind == 'k':
                    moves += self._king_moves(r, c, color)
        return moves

    def _pawn_moves(self, r, c, color):
        moves = []
        p = self.board[r][c]
        d = -1 if color == WHITE else 1
        start_row = 6 if color == WHITE else 1
        promo_row = 0 if color == WHITE else 7

        # forward one
        if self.in_bounds(r + d, c) and self.board[r + d][c] is None:
            if r + d == promo_row:
                for promo in ('q', 'r', 'b', 'n'):
                    moves.append(Move(r, c, r + d, c, p, None, promotion=color + promo))
            else:
                moves.append(Move(r, c, r + d, c, p, None))
            # forward two from start
            if r == start_row and self.board[r + 2 * d][c] is None:
                moves.append(Move(r, c, r + 2 * d, c, p, None))

        # captures
        for dc in (-1, 1):
            rr, cc = r + d, c + dc
            if not self.in_bounds(rr, cc):
                continue
            target = self.board[rr][cc]
            if target is not None and target[0] != color:
                if rr == promo_row:
                    for promo in ('q', 'r', 'b', 'n'):
                        moves.append(Move(r, c, rr, cc, p, target, promotion=color + promo))
                else:
                    moves.append(Move(r, c, rr, cc, p, target))
            elif self.ep_target == (rr, cc):
                captured_pawn = self.board[r][cc]  # the pawn being captured en passant
                moves.append(Move(r, c, rr, cc, p, captured_pawn, is_en_passant=True))
        return moves

    def _knight_moves(self, r, c, color):
        moves = []
        p = self.board[r][c]
        for dr, dc in ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)):
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc):
                target = self.board[rr][cc]
                if target is None or target[0] != color:
                    moves.append(Move(r, c, rr, cc, p, target))
        return moves

    def _sliding_moves(self, r, c, color, dirs):
        moves = []
        p = self.board[r][c]
        for dr, dc in dirs:
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc):
                target = self.board[rr][cc]
                if target is None:
                    moves.append(Move(r, c, rr, cc, p, None))
                else:
                    if target[0] != color:
                        moves.append(Move(r, c, rr, cc, p, target))
                    break
                rr += dr
                cc += dc
        return moves

    def _king_moves(self, r, c, color):
        moves = []
        p = self.board[r][c]
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if self.in_bounds(rr, cc):
                    target = self.board[rr][cc]
                    if target is None or target[0] != color:
                        moves.append(Move(r, c, rr, cc, p, target))

        # castling
        home_row = 7 if color == WHITE else 0
        if r == home_row and c == 4 and not self.in_check(color):
            opp_attacks = self.squares_attacked_by(other(color))
            # king-side
            if self.castling[color + 'K']:
                if self.board[home_row][5] is None and self.board[home_row][6] is None:
                    if self.board[home_row][7] == color + 'r':
                        if (home_row, 5) not in opp_attacks and (home_row, 6) not in opp_attacks:
                            moves.append(Move(r, c, home_row, 6, p, None, is_castle=True))
            # queen-side
            if self.castling[color + 'Q']:
                if (self.board[home_row][1] is None and self.board[home_row][2] is None
                        and self.board[home_row][3] is None):
                    if self.board[home_row][0] == color + 'r':
                        if (home_row, 3) not in opp_attacks and (home_row, 2) not in opp_attacks:
                            moves.append(Move(r, c, home_row, 2, p, None, is_castle=True))
        return moves

    # ---------------------------------------------------------------
    # Legal move generation (pseudo-legal filtered by "king safety")
    # ---------------------------------------------------------------
    def legal_moves(self, color=None):
        color = color or self.turn
        legal = []
        for m in self._pseudo_legal_moves(color):
            self.make_move(m)
            if not self.in_check(color):
                legal.append(m)
            self.undo_move()
        return legal

    def legal_moves_from(self, r, c):
        color = self.turn
        p = self.board[r][c]
        if p is None or p[0] != color:
            return []
        return [m for m in self.legal_moves(color) if m.sr == r and m.sc == c]

    # ---------------------------------------------------------------
    # Make / undo moves
    # ---------------------------------------------------------------
    def make_move(self, move: Move):
        move.prev_castling_rights = dict(self.castling)
        move.prev_ep_target = self.ep_target
        move.prev_halfmove_clock = self.halfmove_clock

        color = move.piece[0]
        kind = move.piece[1]

        # halfmove clock (resets on pawn move or capture)
        if kind == 'p' or move.captured is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # move the piece
        self.board[move.sr][move.sc] = None
        placed_piece = move.promotion if move.promotion else move.piece
        self.board[move.er][move.ec] = placed_piece

        # en passant: remove the captured pawn (which is NOT on the destination square)
        if move.is_en_passant:
            self.board[move.sr][move.ec] = None

        # castling: also move the rook
        if move.is_castle:
            home_row = move.sr
            if move.ec == 6:  # king-side
                self.board[home_row][5] = self.board[home_row][7]
                self.board[home_row][7] = None
            else:  # queen-side
                self.board[home_row][3] = self.board[home_row][0]
                self.board[home_row][0] = None

        # update castling rights
        if kind == 'k':
            self.castling[color + 'K'] = False
            self.castling[color + 'Q'] = False
        if kind == 'r':
            if move.sc == 0:
                self.castling[color + 'Q'] = False
            elif move.sc == 7:
                self.castling[color + 'K'] = False
        # rook captured on its home square also revokes castling rights
        if move.captured is not None and move.captured[1] == 'r':
            if (move.er, move.ec) == (0, 0):
                self.castling['bQ'] = False
            elif (move.er, move.ec) == (0, 7):
                self.castling['bK'] = False
            elif (move.er, move.ec) == (7, 0):
                self.castling['wQ'] = False
            elif (move.er, move.ec) == (7, 7):
                self.castling['wK'] = False

        # set new en-passant target
        if kind == 'p' and abs(move.er - move.sr) == 2:
            self.ep_target = ((move.sr + move.er) // 2, move.sc)
        else:
            self.ep_target = None

        self.turn = other(self.turn)
        self.move_log.append(move)
        self._record_position()

    def undo_move(self):
        if not self.move_log:
            return
        move = self.move_log.pop()
        self._unrecord_position()
        self.turn = other(self.turn)
        color = move.piece[0]

        # restore moved piece
        self.board[move.sr][move.sc] = move.piece
        self.board[move.er][move.ec] = None

        if move.is_en_passant:
            self.board[move.er][move.ec] = None
            self.board[move.sr][move.ec] = move.captured
        else:
            self.board[move.er][move.ec] = move.captured

        if move.is_castle:
            home_row = move.sr
            if move.ec == 6:
                self.board[home_row][7] = self.board[home_row][5]
                self.board[home_row][5] = None
            else:
                self.board[home_row][0] = self.board[home_row][3]
                self.board[home_row][3] = None

        self.castling = move.prev_castling_rights
        self.ep_target = move.prev_ep_target
        self.halfmove_clock = move.prev_halfmove_clock

    # ---------------------------------------------------------------
    # Position repetition tracking (for threefold repetition draws)
    # ---------------------------------------------------------------
    def _position_key(self):
        rows = []
        for r in range(8):
            rows.append(','.join(p or '.' for p in self.board[r]))
        return ('|'.join(rows), self.turn,
                tuple(sorted(self.castling.items())), self.ep_target)

    def _record_position(self):
        key = self._position_key()
        self.position_counts[key] = self.position_counts.get(key, 0) + 1

    def _unrecord_position(self):
        key = self._position_key()
        if key in self.position_counts:
            self.position_counts[key] -= 1
            if self.position_counts[key] <= 0:
                del self.position_counts[key]

    def is_threefold_repetition(self):
        return self.position_counts.get(self._position_key(), 0) >= 3

    def is_fifty_move_draw(self):
        return self.halfmove_clock >= 100  # 50 full moves = 100 half-moves

    # ---------------------------------------------------------------
    # Game-over checks
    # ---------------------------------------------------------------
    def game_status(self):
        """Return one of: 'ongoing', 'checkmate', 'stalemate', 'draw'."""
        moves = self.legal_moves(self.turn)
        if not moves:
            return 'checkmate' if self.in_check(self.turn) else 'stalemate'
        if self.is_fifty_move_draw() or self.is_threefold_repetition():
            return 'draw'
        return 'ongoing'

    # ---------------------------------------------------------------
    # Perft (move-generation correctness test; not used by the GUI)
    # ---------------------------------------------------------------
    def perft(self, depth):
        if depth == 0:
            return 1
        count = 0
        for m in self.legal_moves(self.turn):
            self.make_move(m)
            count += self.perft(depth - 1)
            self.undo_move()
        return count


# ============================================================
#  Self-test (only runs when this file is executed directly
#  with the "--test" flag; the GUI is the default entry point)
# ============================================================
def _run_perft_tests():
    e = ChessEngine()
    # Known perft values for the standard starting position
    expected = {1: 20, 2: 400, 3: 8902, 4: 197281}
    for depth, exp in expected.items():
        got = e.perft(depth)
        status = "OK" if got == exp else "FAIL"
        print(f"perft({depth}) = {got:>7}  (expected {exp:>7})  [{status}]")
        assert got == exp, f"Perft mismatch at depth {depth}"
    print("All perft tests passed — move generation is correct.")


if __name__ == "__main__" and "--test" in sys.argv:
    _run_perft_tests()
    sys.exit(0)

# ============================================================
#  GUI  (pygame front-end) — only imported/run when not testing
# ============================================================
if __name__ != "__main__" or "--test" not in sys.argv:
    import pygame

    BOARD_SIZE = 640
    SQ = BOARD_SIZE // 8
    SIDEBAR = 260
    BOTTOM = 50
    WIDTH = BOARD_SIZE + SIDEBAR
    HEIGHT = BOARD_SIZE + BOTTOM

    LIGHT = (240, 217, 181)
    DARK = (181, 136, 99)
    SELECT_COLOR = (246, 246, 105)
    MOVE_DOT = (60, 60, 60)
    CAPTURE_RING = (200, 60, 60)
    LAST_MOVE = (170, 200, 100)
    CHECK_COLOR = (220, 90, 90)
    BG = (35, 35, 38)
    TEXT_COLOR = (230, 230, 230)
    PANEL_COLOR = (48, 48, 52)

    UNICODE_PIECES = {
        'wk': '\u2654', 'wq': '\u2655', 'wr': '\u2656', 'wb': '\u2657', 'wn': '\u2658', 'wp': '\u2659',
        'bk': '\u265A', 'bq': '\u265B', 'br': '\u265C', 'bb': '\u265D', 'bn': '\u265E', 'bp': '\u265F',
    }

    class ChessGUI:
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Python Chess")
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()

            self.piece_font = self._load_piece_font(int(SQ * 0.72))
            self.ui_font = pygame.font.SysFont("arial", 20)
            self.ui_font_bold = pygame.font.SysFont("arial", 24, bold=True)
            self.small_font = pygame.font.SysFont("arial", 16)

            self.engine = ChessEngine()
            self.selected = None          # (r, c) currently selected square
            self.legal_targets = []       # legal Move objects from selected square
            self.last_move = None
            self.status = 'ongoing'
            self.pending_promotion = None  # Move waiting on a promotion choice
            self.flipped = False           # board orientation

        @staticmethod
        def _load_piece_font(size):
            # Try fonts that reliably include chess glyphs across platforms.
            candidates = ["Segoe UI Symbol", "DejaVu Sans", "Arial Unicode MS", "FreeSerif"]
            for name in candidates:
                try:
                    f = pygame.font.SysFont(name, size)
                    if f.render(UNICODE_PIECES['wk'], True, (0, 0, 0)).get_width() > 2:
                        return f
                except Exception:
                    continue
            return pygame.font.SysFont(None, size)

        # ------------------------------------------------------------
        def screen_to_board(self, x, y):
            if x >= BOARD_SIZE or y >= BOARD_SIZE:
                return None
            c = x // SQ
            r = y // SQ
            if self.flipped:
                r, c = 7 - r, 7 - c
            return int(r), int(c)

        def board_to_screen(self, r, c):
            if self.flipped:
                r, c = 7 - r, 7 - c
            return c * SQ, r * SQ

        # ------------------------------------------------------------
        def draw_board(self):
            for r in range(8):
                for c in range(8):
                    x, y = self.board_to_screen(r, c)
                    color = LIGHT if (r + c) % 2 == 0 else DARK
                    pygame.draw.rect(self.screen, color, (x, y, SQ, SQ))

            # last move highlight
            if self.last_move:
                for (r, c) in [(self.last_move.sr, self.last_move.sc), (self.last_move.er, self.last_move.ec)]:
                    x, y = self.board_to_screen(r, c)
                    s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
                    s.fill((*LAST_MOVE, 130))
                    self.screen.blit(s, (x, y))

            # check highlight
            if self.engine.in_check(self.engine.turn):
                kr, kc = self.engine.king_square(self.engine.turn)
                x, y = self.board_to_screen(kr, kc)
                s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
                s.fill((*CHECK_COLOR, 140))
                self.screen.blit(s, (x, y))

            # selected square highlight
            if self.selected:
                x, y = self.board_to_screen(*self.selected)
                s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
                s.fill((*SELECT_COLOR, 150))
                self.screen.blit(s, (x, y))

            # legal move markers
            for m in self.legal_targets:
                x, y = self.board_to_screen(m.er, m.ec)
                center = (x + SQ // 2, y + SQ // 2)
                if m.captured is not None or m.is_en_passant:
                    pygame.draw.circle(self.screen, CAPTURE_RING, center, SQ // 2 - 4, 4)
                else:
                    pygame.draw.circle(self.screen, MOVE_DOT, center, SQ // 8)

            # coordinates
            files = 'abcdefgh'
            for i in range(8):
                col_index = 7 - i if self.flipped else i
                label = self.small_font.render(files[col_index], True, (90, 90, 90))
                self.screen.blit(label, (i * SQ + SQ - 14, BOARD_SIZE - 16))
                row_index = i if self.flipped else 7 - i
                label2 = self.small_font.render(str(row_index + 1), True, (90, 90, 90))
                self.screen.blit(label2, (4, i * SQ + 2))

        def draw_pieces(self):
            for r in range(8):
                for c in range(8):
                    p = self.engine.board[r][c]
                    if p is None:
                        continue
                    x, y = self.board_to_screen(r, c)
                    glyph = UNICODE_PIECES[p]
                    fill = (250, 250, 250) if p[0] == 'w' else (25, 25, 25)
                    outline = (20, 20, 20) if p[0] == 'w' else (250, 250, 250)
                    # simple outline effect for readability on either square color
                    text = self.piece_font.render(glyph, True, fill)
                    rect = text.get_rect(center=(x + SQ // 2, y + SQ // 2))
                    self.screen.blit(text, rect)

        def draw_sidebar(self):
            panel_rect = (BOARD_SIZE, 0, SIDEBAR, HEIGHT)
            pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect)

            turn_text = "White to move" if self.engine.turn == WHITE else "Black to move"
            if self.status == 'checkmate':
                winner = "Black" if self.engine.turn == WHITE else "White"
                turn_text = f"Checkmate — {winner} wins!"
            elif self.status == 'stalemate':
                turn_text = "Stalemate — draw"
            elif self.status == 'draw':
                turn_text = "Draw"
            elif self.engine.in_check(self.engine.turn):
                turn_text += " (check)"

            title = self.ui_font_bold.render(turn_text, True, TEXT_COLOR)
            self.screen.blit(title, (BOARD_SIZE + 16, 16))

            # move log
            y = 56
            header = self.small_font.render("Moves:", True, (170, 170, 170))
            self.screen.blit(header, (BOARD_SIZE + 16, y))
            y += 22
            log = self.engine.move_log[-20:]
            line = ""
            move_no = max(1, (len(self.engine.move_log) - len(log)) // 2 + 1)
            i = 0
            while i < len(log):
                white_mv = log[i].uci()
                black_mv = log[i + 1].uci() if i + 1 < len(log) else ""
                line = f"{move_no}. {white_mv}  {black_mv}"
                rendered = self.small_font.render(line, True, TEXT_COLOR)
                self.screen.blit(rendered, (BOARD_SIZE + 16, y))
                y += 20
                move_no += 1
                i += 2

            help_lines = [
                "Click a piece, then a",
                "highlighted square to move.",
                "",
                "U — undo last move",
                "R — restart game",
                "F — flip board",
            ]
            y = HEIGHT - 140
            for hl in help_lines:
                rendered = self.small_font.render(hl, True, (150, 150, 150))
                self.screen.blit(rendered, (BOARD_SIZE + 16, y))
                y += 20

        def draw_promotion_menu(self):
            if not self.pending_promotion:
                return
            color = self.pending_promotion.piece[0]
            choices = ['q', 'r', 'b', 'n']
            box_w, box_h = SQ * 4, SQ
            box_x = (BOARD_SIZE - box_w) // 2
            box_y = (BOARD_SIZE - box_h) // 2
            pygame.draw.rect(self.screen, (250, 250, 250), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(self.screen, (20, 20, 20), (box_x, box_y, box_w, box_h), 3)
            self._promo_rects = []
            for i, kind in enumerate(choices):
                cx = box_x + i * SQ
                rect = (cx, box_y, SQ, SQ)
                self._promo_rects.append((rect, color + kind))
                glyph = UNICODE_PIECES[color + kind]
                text = self.piece_font.render(glyph, True, (10, 10, 10))
                trect = text.get_rect(center=(cx + SQ // 2, box_y + SQ // 2))
                self.screen.blit(text, trect)

        # ------------------------------------------------------------
        def handle_click(self, pos):
            if self.pending_promotion:
                for rect, piece_code in self._promo_rects:
                    rx, ry, rw, rh = rect
                    if rx <= pos[0] <= rx + rw and ry <= pos[1] <= ry + rh:
                        self.pending_promotion.promotion = piece_code
                        self.engine.make_move(self.pending_promotion)
                        self.last_move = self.pending_promotion
                        self.pending_promotion = None
                        self.selected = None
                        self.legal_targets = []
                        self.status = self.engine.game_status()
                return

            if self.status != 'ongoing':
                return

            sq = self.screen_to_board(*pos)
            if sq is None:
                return
            r, c = sq

            if self.selected is None:
                piece = self.engine.board[r][c]
                if piece is not None and piece[0] == self.engine.turn:
                    self.selected = (r, c)
                    self.legal_targets = self.engine.legal_moves_from(r, c)
                return

            # a square is already selected
            if (r, c) == self.selected:
                self.selected = None
                self.legal_targets = []
                return

            piece = self.engine.board[r][c]
            if piece is not None and piece[0] == self.engine.turn:
                self.selected = (r, c)
                self.legal_targets = self.engine.legal_moves_from(r, c)
                return

            chosen = None
            for m in self.legal_targets:
                if m.er == r and m.ec == c:
                    chosen = m
                    break

            if chosen is None:
                return

            if chosen.promotion:
                self.pending_promotion = chosen
            else:
                self.engine.make_move(chosen)
                self.last_move = chosen
                self.status = self.engine.game_status()

            self.selected = None
            self.legal_targets = []

        def restart(self):
            self.engine = ChessEngine()
            self.selected = None
            self.legal_targets = []
            self.last_move = None
            self.status = 'ongoing'
            self.pending_promotion = None

        # ------------------------------------------------------------
        def run(self):
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_click(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_u:
                            self.pending_promotion = None
                            self.selected = None
                            self.legal_targets = []
                            self.engine.undo_move()
                            self.last_move = self.engine.move_log[-1] if self.engine.move_log else None
                            self.status = self.engine.game_status()
                        elif event.key == pygame.K_r:
                            self.restart()
                        elif event.key == pygame.K_f:
                            self.flipped = not self.flipped

                self.screen.fill(BG)
                self.draw_board()
                self.draw_pieces()
                self.draw_sidebar()
                self.draw_promotion_menu()
                pygame.display.flip()
                self.clock.tick(60)

            pygame.quit()


def main():
    gui = ChessGUI()
    gui.run()


if __name__ == "__main__":
    main()