def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs) 
        return instances[class_]
    return getinstance

@singleton
class Collider():
    def lidar_colisao(self, o1, o2):
        o1.lidar_colisao(o2)

    def lidar_bola(self, bola, outro):
        outro.lidar_bola(bola)

    def lidar_parede(self, parede, outro):
        outro.lidar_parede(parede)
        
    def lidar_zona(self, zona, outro):
        outro.lidar_zona(zona)
        
    def lidar_buraco(self, buraco, outro):
        outro.lidar_buraco(buraco)

    # --- Lógicas Físicas ---
    def colisao_bola_parede(self, bola, parede):
        bola.vx *= -1
        bola.vy *= -1
        
    def colisao_bola_zona(self, bola, zona):
        bola.vx *= 0.8
        bola.vy *= 0.8
        
    def colisao_bola_buraco(self, bola, buraco):
        # a bola só entra se a velocidade for baixa
        if abs(bola.vx) < 3 and abs(bola.vy) < 3:
            bola.vx = 0
            bola.vy = 0
            bola.coord = list(buraco.coord) 
        return False