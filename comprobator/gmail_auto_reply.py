import time
import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

# Cargar variables de entorno desde .env
load_dotenv()


def analizar_con_chatgpt(consulta):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Crear cliente OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""Xalok es un CMS orientado a medios digitales

El departamento en el que trabajo se encarga de implementar mediante IAC las infraestructuras Cloud donde se ejecuta este CMS, y que estan formadas principalmenente por CDN CloudFront, balanceadores de carga, capas de instancias EC2 autoescalables (capa de cache Varnish, capa de aplicacion, capa de backoffice), AWS RDS con motor MySQL, AWS OpenSearch, Redis, y buckets S3

Estas infraestructuras Cloud de Xalok cuentan con un soporte de mantenimiento MGA en formato 24x7 que permite garantizar la continuidad del servicio gracias a un equipo N1 de monitorización proactiva con capacidad para realizar primeras intervenciones y diagnósticos, y con posibilidad de escalar a un equipo especializado N2 con conocimientos específicos de las infraestructuras.
Tambien existe un sistema automatico de reporte de incidencias mediante Icinga Monitoring System, que reporta las incidencias de tipo Critical y Warning, que llevan en el texto del ticket la palabra "Icinga", si no llevan esa palabra, se considera que son incidencias reportadas por el cliente.
El servicio de soporte cuenta con un SLA que clasifica las incidencias del servicio, y da respuesta y resolución a las mismas según las siguientes tablas.
* ELEMENTOS “VITALES”: Sitio no actualiza, Portada, Boards, Conjunto global de imágenes, Secciones de primer nivel, Directo, Breaking News, Noticia de últimas 24 horas, Publicidad, Sitemap principal de Google, tambien todas as reportadas por Icinga Monitoring System como Critical se considera que afectan a los elementos vitales del sitio.
** El contrato de mantenimiento MGA da soporte a todas aquellas incidencias relacionadas con los recursos y servicios Cloud sobre los que se ejecuta la aplicación de Xalok, quedando fuera de este soporte errores relacionados con el código de la aplicación.
*** Las incidencias de tipo P1 tienen que afectar a todos los usuarios y/o redactores, y ser reproducibles por el equipo de infraestructura para ser consideradas como tales.

P1: Incidencia crítica: Existe un problema grave que afecta a uno o varios de los elementos vitales del site y que impide su visibilidad o actualización. Los elementos vitales son uncamente los indicados anteriormente en la seccion ELEMENTOS VITALES.

P2: Incidencia NO crítica: el rendimiento de la infraestructura está degradado sin afectar al servicio en su totalidad, o alguna de las funcionalidades "no vitales" de la aplicación muestra problemas.

P3: Solicitud o tarea: la plataforma funciona con normalidad, pero existe opción de mejora en la funcionalidad u operatividad.



Tiempos del SLA genérico:
Plazo máx. primera respuesta: P1 - 1 hora, P2 - 6 horas*, P3 - 24 horas*
Plazo máx. resolución: P1 - 4 horas, P2 - 24 horas*, P3: Según disponibilidad
* Dentro del horario de oficina L-V 07:30–19:30 CET

Con toda esta informacion voy a pasarte una incidencia de cliente y necesito que lo clasifiques correctamente, y que tu respuesta sea unicamente P1,P2 o P3 segun corresponda, si ha sido reportada por Icinga y un razonamiento breve de la clasificación:

{consulta}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        resultado = response.choices[0].message.content.strip()
        print(f"{resultado}")
        return resultado
    except Exception as e:
        print(f"Error al llamar a ChatGPT: {e}")
        return "Error"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("parametro", help="Parámetro que será analizado")
    args = parser.parse_args()
    analizar_con_chatgpt(args.parametro)
        
        