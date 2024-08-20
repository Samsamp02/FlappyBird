import pygame, time, random, math

pygame.init
pygame.font.init()
Width, Height = 1000, 800
Window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Flappy Bird")
FONT = pygame.font.SysFont("comicsans", 30)

clock = pygame.time.Clock()
PlayerHeight = 50
PlayerWidth = 70
PipeWidth = 75
PipeHeight = 500
PipeSpeed = 2
PipeIncrement = 300
Gravity = 4 



def draw(player, playerRotate, pipes, Score):
    #background
    background_image = pygame.image.load("bg.png")
    background_image = pygame.transform.scale(background_image, (Width, Height+10)) 
    Window.blit(background_image, (0, 0))
    
  
    #pipes
    for pipe in pipes:
        PipeImage = pygame.image.load('pipe.png')
        PipeImage = pygame.transform.scale(PipeImage, (PipeWidth, PipeHeight))
        #Window.blit(PipeImage, (pipe.x, pipe.y))
        pygame.draw.rect(Window, (0, 255, 0), pipe)
        
    #score
    ScoreText = FONT.render(f"Score: {str(Score)}", 1, (255, 255, 255))
    Window.blit(ScoreText, (Width - 150, 10))


    #player
    #pygame.draw.rect(Window, (175, 175, 175), player)
    Bird = pygame.image.load('bird.png')
    Bird = pygame.transform.scale(Bird, (PlayerWidth, PlayerHeight))
    Bird = pygame.transform.rotozoom(Bird, playerRotate, 1)
    Window.blit(Bird, (player.x, player.y))
    
    pygame.display.update()

def main():
    
    RUN = True
    player = pygame.Rect(Width//5, Height//2, PlayerWidth, PlayerHeight)
    pipes = []
    Jump = False
    JumpMax = 13 
    JumpVel = JumpMax
    PipeCount = 0
    Score = 0
    ElapsedLastJump = 0 
    playerRotate = 0   

    
    while RUN:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False 
                print("Game Over")
                break
        

        #Jumping/Gravity
        ElapsedLastJump += 1
        keys = pygame.key.get_pressed()
        player.y += abs(Gravity + Gravity*ElapsedLastJump/150)
        if player.y > Height + 50:
            RUN = False
            print("Game Over")
            break
        if keys[pygame.K_SPACE] and player.y >-50 and not Jump:
            Jump = True
            ElapsedLastJump = 0

        if Jump:
            player.y -= JumpVel
            JumpVel -= Gravity/17 
            if JumpVel < 5:
                Jump = False
                JumpVel = JumpMax

        #Rotating player
        if Jump and playerRotate < 30:
            playerRotate += 5
        elif not Jump and playerRotate > -45:
            playerRotate -= 2
        
        #Creating pipes
        if PipeCount >= PipeIncrement:
            PipeCount = 0
            PipeHeight = random.randint(15, Height-300)
            UpPipe = pygame.Rect(Width, 0, PipeWidth, PipeHeight)
            DownPipe = pygame.Rect(Width, PipeHeight + 250 - Score, PipeWidth, Height - PipeHeight)
            pipes.append(UpPipe)
            pipes.append(DownPipe)
        else:
            PipeCount += 1

        #Moving pipes
        for pipe in pipes:
            pipe.x -= PipeSpeed
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
            if player.colliderect(pipe):
                print("Game Over")
                RUN = False
                break
        if len(pipes)>0:
            if player.x == pipes[0].x:
                Score += 1

        draw(player, playerRotate, pipes, Score)
        
    pygame.quit()

if (__name__ == "__main__"):
    main()