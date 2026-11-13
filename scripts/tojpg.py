from PIL import Image
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges\web\data")
for n in ["nisar_coh","nisar_hv","nisar_dhv","nisar_comp"]:
    im=Image.open(R/f"{n}.png").convert("RGB")
    im.save(R/f"{n}.jpg",quality=92,optimize=True,progressive=True)
    print(n,(R/f"{n}.jpg").stat().st_size/1e6)
    (R/f"{n}.png").unlink()