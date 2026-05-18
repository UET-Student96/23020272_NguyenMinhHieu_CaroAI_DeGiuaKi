import pygame
import sys
import time

pygame.init()
pygame.font.init()

CELL_SIZE = 40       
BOARD_SIZE = 15      
BOARD_WIDTH = CELL_SIZE * BOARD_SIZE
SIDEBAR_WIDTH = 350  
WINDOW_WIDTH = BOARD_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = CELL_SIZE * BOARD_SIZE

COLOR_BG = (255, 255, 255)
COLOR_GRID = (0, 0, 0)
COLOR_SIDEBAR = (0, 0, 0)
COLOR_X = (0, 0, 255)      
COLOR_O = (255, 0, 0)      
COLOR_TEXT = (255, 255, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Trò chơi Cờ Caro - Hệ thống AI")

sys_fonts = pygame.font.get_fonts()
best_font = "arial"
for f in ["tahoma", "segoeui", "calibri", "arial", "timesnewroman"]:
    if f in sys_fonts:
        best_font = f
        break

font_btn = pygame.font.SysFont(best_font, 22, bold=True)
font_sm = pygame.font.SysFont(best_font, 16)

class CaroAI:
    def __init__(self, size=15):
        self.size = size
        self.ai_mode = "Alpha-Beta" 
        self.depth = 2          
        self.ai_active = True   
        self.reset()

    def reset(self):
        self.board = [['.' for _ in range(self.size)] for _ in range(self.size)]
        self.history = []       
        self.current_turn = 'X' 
        self.states_cnt = 0
        
        if self.ai_active:
            self.log_msg = ["Chế độ: ĐẤU VỚI AI", "Trạng thái AI: Sẵn sàng", "Thời gian phản ứng: 0.0000s", ""]
        else:
            self.log_msg = ["Chế độ: NGƯỜI VS NGƯỜI", "Lượt đi hiện tại: X", "Bắt đầu trận đấu mới!", ""]

    def is_valid_move(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == '.'

    def make_move(self, r, c, symbol):
        self.board[r][c] = symbol
        self.history.append((r, c, symbol))

    def undo_move(self):
        if len(self.history) > 0:
            if self.ai_active:
                if len(self.history) >= 2:
                    for _ in range(2):
                        r, c, _ = self.history.pop()
                        self.board[r][c] = '.'
                    self.current_turn = 'X'
            else:
                r, c, _ = self.history.pop()
                self.board[r][c] = '.'
                self.current_turn = 'O' if self.current_turn == 'X' else 'X'

    def check_win(self, symbol):
        for r in range(self.size):
            for c in range(self.size - 3):
                if all(self.board[r][c+i] == symbol for i in range(4)): return True
        for r in range(self.size - 3):
            for c in range(self.size):
                if all(self.board[r+i][c] == symbol for i in range(4)): return True
        for r in range(self.size - 3):
            for c in range(self.size - 3):
                if all(self.board[r+i][c+i] == symbol for i in range(4)): return True
        for r in range(3, self.size):
            for c in range(self.size - 3):
                if all(self.board[r-i][c+i] == symbol for i in range(4)): return True
        return False

    def is_full(self):
        return all(self.board[r][c] != '.' for r in range(self.size) for c in range(self.size))

    def get_ordered_moves(self):
        move_scores = []
        has_pieces = False
        
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != '.':
                    has_pieces = True
                    break
            if has_pieces:
                break
                
        if not has_pieces:
            return [(self.size // 2, self.size // 2)]

        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    neighbor_score = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.board[nr][nc] != '.':
                                    neighbor_score += 1
                    if neighbor_score > 0:
                        move_scores.append(((r, c), neighbor_score))
                        
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, score in move_scores]

    def evaluate_line(self, line, ai_s, pl_s):
        score = 0
        ai_c = line.count(ai_s)
        pl_c = line.count(pl_s)
        em_c = line.count('.')
        
        if ai_c == 4: return 100000
        if pl_c == 4: return -100000
        if ai_c == 3 and em_c == 1: score += 500
        elif pl_c == 3 and em_c == 1: score -= 900  
        if ai_c == 2 and em_c == 2: score += 50
        elif pl_c == 2 and em_c == 2: score -= 80
        return score

    def evaluate_board(self):
        score = 0
        ai_s, pl_s = 'O', 'X'
        for r in range(self.size):
            for c in range(self.size - 3):
                score += self.evaluate_line([self.board[r][c+i] for i in range(4)], ai_s, pl_s)
        for r in range(self.size - 3):
            for c in range(self.size):
                score += self.evaluate_line([self.board[r+i][c] for i in range(4)], ai_s, pl_s)
        for r in range(self.size - 3):
            for c in range(self.size - 3):
                score += self.evaluate_line([self.board[r+i][c+i] for i in range(4)], ai_s, pl_s)
        for r in range(3, self.size):
            for c in range(self.size - 3):
                score += self.evaluate_line([self.board[r-i][c+i] for i in range(4)], ai_s, pl_s)
        return score

    def minimax(self, depth, is_max):
        self.states_cnt += 1
        if self.check_win('O'): return 100000 + depth
        if self.check_win('X'): return -100000 - depth
        if self.is_full() or depth == 0: return self.evaluate_board()

        valid_moves = self.get_ordered_moves()
        if is_max:
            best = -float('inf')
            for r, c in valid_moves:
                self.board[r][c] = 'O'
                best = max(best, self.minimax(depth - 1, False))
                self.board[r][c] = '.'
            return best
        else:
            best = float('inf')
            for r, c in valid_moves:
                self.board[r][c] = 'X'
                best = min(best, self.minimax(depth - 1, True))
                self.board[r][c] = '.'
            return best

    def alphabeta(self, depth, alpha, beta, is_max):
        self.states_cnt += 1
        if self.check_win('O'): return 100000 + depth
        if self.check_win('X'): return -100000 - depth
        if self.is_full() or depth == 0: return self.evaluate_board()

        valid_moves = self.get_ordered_moves()
        if is_max:
            best = -float('inf')
            for r, c in valid_moves:
                self.board[r][c] = 'O'
                score = self.alphabeta(depth - 1, alpha, beta, False)
                self.board[r][c] = '.'
                best = max(best, score)
                alpha = max(alpha, score)
                if beta <= alpha: break
            return best
        else:
            best = float('inf')
            for r, c in valid_moves:
                self.board[r][c] = 'X'
                score = self.alphabeta(depth - 1, alpha, beta, True)
                self.board[r][c] = '.'
                best = min(best, score)
                beta = min(beta, score)
                if beta <= alpha: break
            return best

    def ai_play(self):
        self.states_cnt = 0
        start = time.time()
        best_score = -float('inf')
        best_move = None
        valid_moves = self.get_ordered_moves()

        for r, c in valid_moves:
            self.board[r][c] = 'O'
            if self.ai_mode == "Minimax":
                score = self.minimax(self.depth - 1, False)
            else:
                score = self.alphabeta(self.depth - 1, -float('inf'), float('inf'), False)
            self.board[r][c] = '.'

            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        dur = time.time() - start

        if best_move:
            self.make_move(best_move[0], best_move[1], 'O')
            self.log_msg = [
                f"AI Thuật toán: {self.ai_mode}",
                f"Số trạng thái đã xét: {self.states_cnt}",
                f"Thời gian phản ứng: {dur:.4f}s", 
                ""
            ]

def draw_gui(game):
    screen.fill(COLOR_BG)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)
            
            if game.board[r][c] == 'X':
                txt = font_btn.render("X", True, COLOR_X)
                screen.blit(txt, (c * CELL_SIZE + 13, r * CELL_SIZE + 8))
            elif game.board[r][c] == 'O':
                txt = font_btn.render("O", True, COLOR_O)
                screen.blit(txt, (c * CELL_SIZE + 12, r * CELL_SIZE + 8))

    sidebar_rect = pygame.Rect(BOARD_WIDTH, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COLOR_SIDEBAR, sidebar_rect)

    pygame.draw.rect(screen, (30, 30, 50), (BOARD_WIDTH + 110, 20, 130, 45), 0, 5)
    pygame.draw.rect(screen, (0, 150, 255), (BOARD_WIDTH + 110, 20, 130, 45), 2, 5)
    lbl_ai = font_btn.render("AI v1.0", True, (0, 200, 255))
    screen.blit(lbl_ai, (BOARD_WIDTH + 145, 30))

    color_ai_btn = (0, 160, 0) if game.ai_active else (60, 60, 60)
    pygame.draw.rect(screen, color_ai_btn, (BOARD_WIDTH + 50, 85, 115, 45), 0, 4)
    pygame.draw.rect(screen, (255, 255, 255), (BOARD_WIDTH + 50, 85, 115, 45), 2, 4)
    txt_ai = font_btn.render("AI Mode", True, COLOR_TEXT)
    screen.blit(txt_ai, (BOARD_WIDTH + 68, 95))

    color_p2p_btn = (0, 160, 0) if not game.ai_active else (60, 60, 60)
    pygame.draw.rect(screen, color_p2p_btn, (BOARD_WIDTH + 185, 85, 115, 45), 0, 4)
    pygame.draw.rect(screen, (255, 255, 255), (BOARD_WIDTH + 185, 85, 115, 45), 2, 4)
    txt_p2p = font_btn.render("P v P", True, COLOR_TEXT)
    screen.blit(txt_p2p, (BOARD_WIDTH + 220, 95))

    disabled_color = (35, 35, 35)

    modes = [("E", 1), ("M", 2), ("H", 3)]
    for i, (char, d) in enumerate(modes):
        bx = BOARD_WIDTH + 55 + i * 85
        if game.ai_active:
            color_b = (200, 120, 0) if game.depth == d else (50, 50, 50)
        else:
            color_b = disabled_color
        pygame.draw.rect(screen, color_b, (bx, 150, 65, 45), 0, 4)
        pygame.draw.rect(screen, (150, 150, 150) if game.ai_active else (80, 80, 80), (bx, 150, 65, 45), 2, 4)
        txt_c = font_btn.render(char, True, COLOR_TEXT if game.ai_active else (100, 100, 100))
        screen.blit(txt_c, (bx + 26, 160))

    if game.ai_active:
        color_mm = (120, 0, 120) if game.ai_mode == "Minimax" else (50, 50, 50)
        color_ab = (120, 0, 120) if game.ai_mode == "Alpha-Beta" else (50, 50, 50)
    else:
        color_mm = disabled_color
        color_ab = disabled_color

    pygame.draw.rect(screen, color_mm, (BOARD_WIDTH + 50, 215, 115, 45), 0, 4)
    pygame.draw.rect(screen, (255, 255, 255) if game.ai_active else (80, 80, 80), (BOARD_WIDTH + 50, 215, 115, 45), 2, 4)
    txt_mm = font_btn.render("Minimax", True, COLOR_TEXT if game.ai_active else (100, 100, 100))
    screen.blit(txt_mm, (BOARD_WIDTH + 62, 225))

    pygame.draw.rect(screen, color_ab, (BOARD_WIDTH + 185, 215, 115, 45), 0, 4)
    pygame.draw.rect(screen, (255, 255, 255) if game.ai_active else (80, 80, 80), (BOARD_WIDTH + 185, 215, 115, 45), 2, 4)
    txt_ab = font_btn.render("A-B Prun", True, COLOR_TEXT if game.ai_active else (100, 100, 100))
    screen.blit(txt_ab, (BOARD_WIDTH + 198, 225))

    pygame.draw.rect(screen, (30, 100, 200), (BOARD_WIDTH + 50, 285, 250, 50), 0, 6)
    pygame.draw.rect(screen, (255, 255, 255), (BOARD_WIDTH + 50, 285, 250, 50), 3, 6)
    txt_undo = font_btn.render("UNDO", True, COLOR_TEXT)
    screen.blit(txt_undo, (BOARD_WIDTH + 148, 298))

    pygame.draw.rect(screen, (200, 30, 30), (BOARD_WIDTH + 50, 355, 250, 50), 0, 6)
    pygame.draw.rect(screen, (255, 255, 255), (BOARD_WIDTH + 50, 355, 250, 50), 3, 6)
    txt_exit = font_btn.render("EXIT", True, COLOR_TEXT)
    screen.blit(txt_exit, (BOARD_WIDTH + 153, 368))

    pygame.draw.rect(screen, (220, 140, 10), (BOARD_WIDTH + 50, 425, 250, 50), 0, 6)
    pygame.draw.rect(screen, (255, 255, 255), (BOARD_WIDTH + 50, 425, 250, 50), 3, 6)
    txt_replay = font_btn.render("REPLAY", True, COLOR_TEXT)
    screen.blit(txt_replay, (BOARD_WIDTH + 138, 438))

    log_box = pygame.Rect(BOARD_WIDTH + 30, 505, 290, 85)
    pygame.draw.rect(screen, (20, 20, 20), log_box, 0, 4)
    pygame.draw.rect(screen, (0, 255, 0), log_box, 1, 4)  
    
    for idx, msg in enumerate(game.log_msg):
        rendered_msg = font_sm.render(msg, True, (0, 255, 0))
        screen.blit(rendered_msg, (BOARD_WIDTH + 40, 512 + idx * 18))

    pygame.display.flip()

def main():
    game = CaroAI(size=BOARD_SIZE)
    gameover = False

    while True:
        draw_gui(game)

        if game.ai_active and game.current_turn == 'O' and not gameover:
            game.ai_play()
            if game.check_win('O'):
                game.log_msg = ["MÁY TÍNH (O) CHIẾN THẮNG!", "Bấm REPLAY để làm ván mới.", "", ""]
                gameover = True
            elif game.is_full():
                game.log_msg = ["TRẬN ĐẤU HÒA!", "Bàn cờ đã đầy.", "", ""]
                gameover = True
            else:
                game.current_turn = 'X'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()

                if mx < BOARD_WIDTH and not gameover:
                    c = mx // CELL_SIZE
                    r = my // CELL_SIZE
                    if game.is_valid_move(r, c):
                        game.make_move(r, c, game.current_turn)
                        
                        if game.check_win(game.current_turn):
                            game.log_msg = [f"NGƯỜI CHƠI ({game.current_turn}) CHIẾN THẮNG!", "Trận đấu kết thúc.", "", ""]
                            gameover = True
                        elif game.is_full():
                            game.log_msg = ["TRẬN ĐẤU HÒA!", "", "", ""]
                            gameover = True
                        else:
                            if game.ai_active:
                                game.current_turn = 'O'  
                            else:
                                game.current_turn = 'O' if game.current_turn == 'X' else 'X'
                                game.log_msg = ["Chế độ: NGƯỜI VS NGƯỜI", f"Lượt đi hiện tại: {game.current_turn}", "", ""]

                elif mx >= BOARD_WIDTH:
                    if BOARD_WIDTH + 50 <= mx <= BOARD_WIDTH + 165 and 85 <= my <= 130:
                        game.ai_active = True
                        game.reset()  
                        gameover = False
                    
                    elif BOARD_WIDTH + 185 <= mx <= BOARD_WIDTH + 300 and 85 <= my <= 130:
                        game.ai_active = False
                        game.reset()  
                        gameover = False

                    if game.ai_active:
                        if 150 <= my <= 195:
                            if BOARD_WIDTH + 55 <= mx <= BOARD_WIDTH + 120:   game.depth = 1
                            elif BOARD_WIDTH + 140 <= mx <= BOARD_WIDTH + 205: game.depth = 2
                            elif BOARD_WIDTH + 225 <= mx <= BOARD_WIDTH + 290: game.depth = 3
                        
                        elif BOARD_WIDTH + 50 <= mx <= BOARD_WIDTH + 165 and 215 <= my <= 260:
                            game.ai_mode = "Minimax"
                        
                        elif BOARD_WIDTH + 185 <= mx <= BOARD_WIDTH + 300 and 215 <= my <= 260:
                            game.ai_mode = "Alpha-Beta"

                    if BOARD_WIDTH + 50 <= mx <= BOARD_WIDTH + 300 and 285 <= my <= 335:
                        game.undo_move()
                        gameover = False
                        if game.ai_active:
                            game.log_msg = ["Đã hoàn tác (Undo) 1 lượt chơi!"]
                        else:
                            game.log_msg = ["Chế độ: NGƯỜI VS NGƯỜI", f"Lượt đi hiện tại: {game.current_turn}", "Đã hoàn tác nước đi!", ""]

                    elif BOARD_WIDTH + 50 <= mx <= BOARD_WIDTH + 300 and 355 <= my <= 405:
                        pygame.quit()
                        sys.exit()

                    elif BOARD_WIDTH + 50 <= mx <= BOARD_WIDTH + 300 and 425 <= my <= 475:
                        game.reset()
                        gameover = False

if __name__ == "__main__":
    main()