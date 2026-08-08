import requests
import time

# ========== CONFIGURADO ==========
UNIVERSE_ID = 7219654364
WEBHOOK_URL = "https://discord.com/api/webhooks/1535754404202942595/6TCxhQkieK0HWzKRdJAcg8xYWSfJ1odjrympGYvuCjVpxeeyc5fDrOowIqEiEStcb8Tl"
CHECK_INTERVAL = 60  # 1 minuto
# ================================

last_updated = None

def check_update():
    global last_updated
    url = f"https://games.roblox.com/v1/games?universeIds={UNIVERSE_ID}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()["data"][0]
        
        current_updated = data["updated"]
        name = data["name"]
        playing = data["playing"]
        visits = data["visits"]
        
        if last_updated is None:
            last_updated = current_updated
            print(f"Monitor iniciado: {name}")
            print(f"Última actualización: {current_updated}")
            return
        
        if current_updated != last_updated:
            print(f"¡Actualización detectada! {name}")
            
            embed = {
                "title": f"🟢 {name} se actualizó",
                "description": f"**Nueva fecha:** `{current_updated}`\n**Anterior:** `{last_updated}`",
                "color": 5763719,
                "fields": [
                    {"name": "Jugadores ahora", "value": f"{playing:,}", "inline": True},
                    {"name": "Visitas totales", "value": f"{visits:,}", "inline": True}
                ],
                "url": "https://www.roblox.com/games/135856908115931/Murderers-VS-Sheriffs"
            }
            
            requests.post(WEBHOOK_URL, json={
                "content": "@everyone",
                "embeds": [embed]
            })
            
            last_updated = current_updated
            
    except Exception as e:
        print("Error:", e)

print("Monitor de Murderers VS Sheriffs iniciado...")
while True:
    check_update()
    time.sleep(CHECK_INTERVAL)
