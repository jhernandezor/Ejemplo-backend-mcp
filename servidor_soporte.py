import json
import pymysql
from mcp.server.mcpserver import MCPServer

# 1. Instanciar el servidor MCP
mcp = MCPServer("Servidor Soporte FCE")

# 2. Conexión a la base de datos MySQL local
def obtener_conexion():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="123456789",          # Si tu MySQL tiene contraseña, colócala entre las comillas
        database="fce_soporte",
        cursorclass=pymysql.cursors.DictCursor
    )

# 3. Herramienta para consultar tickets
@mcp.tool()
def listar_tickets() -> str:
    """Obtiene la lista completa de tickets registrados en el sistema de soporte en formato JSON."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, asunto, descripcion, fecha_creacion FROM tickets ORDER BY id DESC")
            registros = cursor.fetchall()
            
            # Formatear fechas a string para evitar errores de serialización
            for r in registros:
                if r.get("fecha_creacion") is not None:
                    r["fecha_creacion"] = str(r["fecha_creacion"])
                    
            return json.dumps(registros, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conexion.close()

# 4. Herramienta para registrar tickets
@mcp.tool()
def crear_ticket(asunto: str, descripcion: str) -> str:
    """Registra un nuevo ticket de soporte en la base de datos MySQL.

    Args:
        asunto: Titulo o problema resumido del ticket.
        descripcion: Detalle completo de la falla o requerimiento.
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO tickets (asunto, descripcion) VALUES (%s, %s)"
            cursor.execute(sql, (asunto, descripcion))
            conexion.commit()
            nuevo_id = cursor.lastrowid
            return json.dumps({
                "status": "exito",
                "mensaje": f"Ticket #{nuevo_id} guardado correctamente",
                "id": nuevo_id
            }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conexion.close()

if __name__ == "__main__":
    mcp.run()