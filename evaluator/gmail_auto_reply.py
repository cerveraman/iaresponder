import time
import os
from dotenv import load_dotenv
from openai import OpenAI
import mysql.connector


# Cargar variables de entorno desde .env
load_dotenv()

def run_query(query: str):
    # Lee las credenciales de MySQL
    db_config = {
        'host': os.getenv("MYSQL_HOST"),
        'user': os.getenv("MYSQL_USER"),
        'password': os.getenv("MYSQL_PASSWORD"),
        'database': os.getenv("MYSQL_DATABASE"),
        'port': int(os.getenv("MYSQL_PORT", 3306)),
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT ticketid FROM swtickets WHERE departmenttitle = "Area Xalok" AND ticketstatustitle = "Abierto" AND dateline <= UNIX_TIMESTAMP(NOW()) - 60 AND laststaffreplytime = 0')
        result = cursor.fetchall()
        cursor.close()
        for row in result:
            cursor = conn.cursor()
            cursor.execute('SELECT contents FROM swticketposts where ticketid = ' + str(row[0]))
            contenido = cursor.fetchall()
            print(contenido[0][0])
            cursor.close()

            insertar_nota(str(row[0]), analizar_con_chatgpt(contenido[0][0]) )
        
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def analizar_con_chatgpt(consulta):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Crear cliente OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""Xalok es un CMS orientado a medios digitales

El departamento en el que trabajo se encarga de implementar mediante IAC las infraestructuras Cloud donde se ejecuta este CMS, y que estan formadas principalmenente por CDN CloudFront, balanceadores de carga, capas de instancias EC2 autoescalables (capa de cache Varnish, capa de aplicacion, capa de backoffice), AWS RDS con motor MySQL, AWS OpenSearch, Redis, y buckets S3

Estas infraestructuras Cloud de Xalok cuentan con un soporte de mantenimiento MGA en formato 24x7 que permite garantizar la continuidad del servicio gracias a un equipo N1 de monitorización proactiva con capacidad para realizar primeras intervenciones y diagnósticos, y con posibilidad de escalar a un equipo especializado N2 con conocimientos específicos de las infraestructuras.

El servicio de soporte cuenta con un SLA que clasifica las incidencias del servicio, y da respuesta y resolución a las mismas según las siguientes tablas.
* ELEMENTOS “VITALES”: Sitio no actualiza, Portada, Boards, Conjunto global de imágenes, Secciones de primer nivel, Directo, Breaking News, Noticia de últimas 24 horas, Publicidad, Sitemap principal de Google.
** El contrato de mantenimiento MGA da soporte a todas aquellas incidencias relacionadas con los recursos y servicios Cloud sobre los que se ejecuta la aplicación de Xalok, quedando fuera de este soporte errores relacionados con el código de la aplicación.
*** Las incidencias de tipo P1 tienen que afectar a todos los usuarios y/o redactores, y ser reproducibles por el equipo de infraestructura para ser consideradas como tales.

P1: Incidencia crítica: Existe un problema grave que afecta a uno o varios de los elementos vitales del site y que impide su visibilidad o actualización

P2: Incidencia NO crítica: el rendimiento de la infraestructura está degradado sin afectar al servicio en su totalidad, o alguna de las funcionalidades "no vitales" de la aplicación muestra problemas.

P3: Solicitud o tarea: la plataforma funciona con normalidad, pero existe opción de mejora en la funcionalidad u operatividad.



Tiempos del SLA genérico:
Plazo máx. primera respuesta: P1 - 1 hora, P2 - 6 horas*, P3 - 24 horas*
Plazo máx. resolución: P1 - 4 horas, P2 - 24 horas*, P3: Según disponibilidad
* Dentro del horario de oficina L-V 07:30–19:30 CET

Con toda esta informacion voy a pasarte una incidencia de cliente y necesito que lo clasifiques correctamente, y que tu respuesta siempre comience por la frase Esta incidencia ha sido clasificada por IA, seguido por Prioridad y P1, P2 o P3 segun corresponda, seguido por DEBE ESCALARSE si esta clasificada como P1 y NO DEBE ESCALARSE si no lo es  y después des una explicación de menos de 100 palabras de por que se ha clasificado así. La descripción del ticket es la siguiente:"

{consulta}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        resultado = response.choices[0].message.content.strip()
        print(f"{resultado}")
        return resultado
    except Exception as e:
        print(f"Error al llamar a ChatGPT: {e}")
        return "Error"

def insertar_nota(linktypeid, note):
    db_config = {
        'host': os.getenv("MYSQL_HOST"),
        'user': os.getenv("MYSQL_USER"),
        'password': os.getenv("MYSQL_PASSWORD"),
        'database': os.getenv("MYSQL_DATABASE"),
        'port': int(os.getenv("MYSQL_PORT", 3306)),
    }
    try:
        conn = mysql.connector.connect(**db_config)

        cursor = conn.cursor()

        query = """
        INSERT INTO swticketnotes (
            linktypeid, linktype, forstaffid, staffid, dateline, isedited, 
            staffname, editedstaffid, editedstaffname, editedtimeline, notecolor, note
        ) VALUES (
            %s, 1, 0, 385, UNIX_TIMESTAMP(), 0, 
            '', 0, '', 0, 1, %s
        );
        """

        cursor.execute(query, (linktypeid, note))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error al insertar nota: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    QUERY = 'SELECT * FROM swtickets WHERE departmenttitle = "Area Xalok" AND ticketstatustitle = "Abierto" AND laststaffreplytime = 0'  # Cambia por tu consulta
    while True:
        run_query(QUERY)
        #analizar_con_chatgpt("se ha caido el site, no puedo acceder a nada")
        time.sleep(300)