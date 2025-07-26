# MinTrabajo – Consulta Masiva de Cursos

Este proyecto automatiza la consulta de certificados de formación en 
la web del Ministerio de Trabajo de Colombia.

- **Consulta**: lee cédulas de `cedulas.txt`  
- **Output**: genera `resultados.csv` con columnas `cedula,nombre,cursos`

## Uso

```bash
git clone https://github.com/<tu-usuario>/mintrabajo-consultas.git
cd mintrabajo-consultas
pip install -r requirements.txt
python consulta_cursos.py
```

## GitHub Pages

La documentación está en `/docs/index.md` y se publica automáticamente 
en https://<tu-usuario>.github.io/mintrabajo-consultas/
