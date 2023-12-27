import pygame
from particle import Particle
pygame.init()
#ciao sono cicciogamer

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Collision Simulation')

FPS = 180
WHITE = (255, 255, 255)

MAX_PARTICLES = 1000
collision_counter = 0


def draw_window(particles: list):
    WIN.fill(WHITE)

    for particle in particles:
        pygame.draw.ellipse(WIN, particle.color, particle)

    pygame.display.update()


def handle_particles_movement(particles):
    for particle in particles:
        if (particle.left + particle.vel_x) < 0 or (particle.right + particle.vel_x) > WIDTH:
            particle.vel_x = - particle.vel_x
        if (particle.top + particle.vel_y) < 0 or (particle.bottom + particle.vel_y) > HEIGHT:
            particle.vel_y = - particle.vel_y
        particle.move_ip(particle.vel_x, particle.vel_y)
    pygame.display.update()


def check_for_collisions(particles, collisions):
    global collision_counter
    for i in range(len(particles)):
        particle = particles[i]
        for j in range(i + 1, len(particles)):
            collided_particle = particles[j]
            if particle.colliderect(collided_particle):
                collision_counter+=1
                collisions.append((particle, collided_particle))


def set_velocity_after_collision(particle1: Particle, particle2: Particle):
    # Calcolare velocità del centro di massa dell'asse x
    # Calcolare velocità del centro di massa dell'asse y
    vcm_x = (particle1.mass*particle1.vel_x + particle2.mass *
             particle2.vel_x)/(particle1.mass + particle2.mass)
    vcm_y = (particle1.mass*particle1.vel_y + particle2.mass *
             particle2.vel_y)/(particle1.mass + particle2.mass)
    # Sottrarre le rispettive velocità del centro di massa alle velocità dell'asse x e y
    vel_rel_1_x = particle1.vel_x - vcm_x
    vel_rel_1_y = particle1.vel_y - vcm_y

    vel_rel_2_x = particle2.vel_x - vcm_x
    vel_rel_2_y = particle2.vel_y - vcm_y
    # Trovare le velocità relative finali del centro di massa moltiplicando le velocità relative iniziali per -1
    vel_rel_2_x_final = - vel_rel_2_x
    vel_rel_2_y_final = - vel_rel_2_y

    vel_rel_1_x_final = - vel_rel_1_x
    vel_rel_1_y_final = - vel_rel_1_y
    # Trovare le velocità finali sommando alle velocità relative finali la velocità del centro di massa

    vel_1_x_final = vel_rel_1_x_final + vcm_x
    vel_1_y_final = vel_rel_1_y_final + vcm_y

    vel_2_x_final = vel_rel_2_x_final + vcm_x
    vel_2_y_final = vel_rel_2_y_final + vcm_y

    particle1.update_velocity(vel_1_x_final, vel_1_y_final)
    particle2.update_velocity(vel_2_x_final, vel_2_y_final)


def handle_collisions(collisions):
    for collision in collisions:
        first_particle = collision[0]
        second_particle = collision[1]
        set_velocity_after_collision(first_particle, second_particle)
        while first_particle.colliderect(second_particle):
            if first_particle.x < second_particle.x:
                first_particle.x -= second_particle.width
            else:
                first_particle.x += second_particle.width
    collisions.clear()


def main():
    running = True
    clock = pygame.time.Clock()
    # Creazione di due particelle iniziali nella simulazione
    particles = [Particle.get_particle(), Particle.get_particle()]
    collisions = []

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print('Total collisions:', collision_counter)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL and len(particles) < MAX_PARTICLES:
                    particles.append(Particle.get_particle())

        if running:
            handle_particles_movement(particles)
            check_for_collisions(particles, collisions)
            handle_collisions(collisions)
            draw_window(particles)


if __name__ == '__main__':
    main()


"""
BUG:

 Quando il numero di particelle e quindi collisioni aumenta allora, a volte, una coppia di particelle
   si "attacca" e poi si separa dopo pochi secondi, permettendo alle particelle di continuare 
   il loro moto individuale.

   In teoria questo bug si verifica perchè, quando ci sono molte particelle, il programma non riesce 
   ad aggiornare immediatamente la velocità delle particelle dopo la collisione e quindi si sovrappongono e ciò comporta una 
   registrazione continua di collisioni da parte del programma, quindi un aggiornamento continuo di velocità
   probabilmente opposte per le equazioni fisiche degli urti. In questo modo si verifica un "attaccamento"
   delle particelle ed un "tremolio continuo" tra le due. -> SEMI RISOLTO

"""
