# Taller AI Prediqt

> Taller práctico de **Agentic AI con Claude Code**: construcción de un flujo de análisis SQL que integra Skills, Subagents, MCP Servers y Hooks.

---

## 1. Descripción

**Taller AI Prediqt** es un proyecto guiado de 2 horas para aprender a extender Claude Code con sus cuatro mecanismos principales de personalización. A lo largo del taller se construye un asistente de análisis SQL que consulta una base de datos de prueba, aplica estándares de calidad y opera bajo reglas de seguridad definidas por el equipo.

El proyecto prioriza una arquitectura mínima: un componente de cada tipo, configurado según las convenciones oficiales de Claude Code y versionado con Git y GitHub.

## 2. Objetivo

**Qué se construye:** un flujo de trabajo agéntico capaz de responder preguntas de negocio mediante consultas SQL seguras, legibles y bien documentadas.

**Qué se aprende:**

- Definir conocimiento reutilizable con un **Skill** (estándares SQL).
- Delegar tareas especializadas a un **Subagent** con contexto y herramientas propias.
- Conectar Claude Code a fuentes de datos externas mediante un **MCP Server**.
- Aplicar controles deterministas de seguridad con un **Hook**.
- Versionar y compartir la configuración del equipo con **Git y GitHub**.

## 3. Tecnologías utilizadas

| Tecnología | Rol en el proyecto |
|---|---|
| **Claude Code** | Agente principal que orquesta el flujo de análisis. |
| **VS Code** | Entorno de desarrollo con la extensión de Claude Code. |
| **Skills** | Estándares y buenas prácticas SQL cargados bajo demanda. |
| **Subagents** | Analista SQL especializado con contexto aislado. |
| **MCP Servers** | Conexión a la base de datos de prueba (SQLite). |
| **Hooks** | Validación previa que bloquea operaciones SQL destructivas. |
| **Git** | Control de versiones local del proyecto. |
| **GitHub** | Repositorio remoto para compartir la configuración y colaborar. |

## 4. Estructura del proyecto

```text
taller-ai-prediqt/
├── .claude/
│   ├── agents/
│   │   └── sql-analyst.md          # Subagent: analista SQL (usa el Skill)
│   ├── skills/
│   │   └── sql-standards/
│   │       └── SKILL.md            # Skill: estándares y buenas prácticas SQL
│   ├── hooks/
│   │   └── block-destructive-sql.sh # Hook: bloquea DROP, DELETE, TRUNCATE, etc.
│   └── settings.json               # Registro del Hook (PreToolUse) y permisos
├── data/
│   └── sample.db                   # Base de datos SQLite de prueba
├── .mcp.json                       # MCP Server: conexión a data/sample.db
├── .gitignore                      # Exclusiones de Git
├── CLAUDE.md                       # Contexto e instrucciones del proyecto
└── README.md                       # Documentación del proyecto
```

| Componente | Archivo | Propósito |
|---|---|---|
| Skill | `.claude/skills/sql-standards/SKILL.md` | Convenciones de nombres, formato, uso de CTEs, filtros explícitos y comentarios. |
| Subagent | `.claude/agents/sql-analyst.md` | Traduce preguntas de negocio a SQL, ejecuta consultas e interpreta resultados aplicando el Skill. |
| MCP Server | `.mcp.json` | Configura un servidor MCP de SQLite con alcance de proyecto. |
| Hook | `.claude/hooks/block-destructive-sql.sh` + `.claude/settings.json` | Inspecciona cada consulta antes de ejecutarla y la bloquea si es destructiva. |
| Git / GitHub | `.gitignore`, `CLAUDE.md`, `README.md` | Versionado, contexto compartido y documentación. |

## 5. Flujo de trabajo

```text
Usuario ──► Claude Code ──► Subagent sql-analyst ──► Hook (PreToolUse) ──► MCP Server ──► sample.db
                                  │                        │
                          aplica Skill               ¿consulta destructiva?
                          sql-standards              Sí → bloquea  ·  No → permite
```

1. **Solicitud:** el usuario plantea una pregunta de negocio en Claude Code (por ejemplo, *"¿Cuáles son los 5 productos con mayores ventas?"*).
2. **Delegación:** Claude Code delega la tarea al **Subagent** `sql-analyst`.
3. **Estándares:** el Subagent carga el **Skill** `sql-standards` y redacta una consulta conforme a las buenas prácticas.
4. **Control:** antes de ejecutarla, el **Hook** `PreToolUse` revisa la sentencia; si contiene `DROP`, `DELETE`, `TRUNCATE`, `ALTER` o `UPDATE`, la bloquea y devuelve el motivo.
5. **Ejecución:** si la consulta es segura, el **MCP Server** la ejecuta sobre `sample.db` y devuelve los resultados.
6. **Respuesta:** el Subagent interpreta los datos y entrega la consulta, los resultados y las conclusiones al usuario.

## 6. Resultado esperado

Al finalizar el taller, el proyecto permitirá:

- Formular preguntas de negocio en lenguaje natural y obtener consultas SQL ejecutadas sobre datos reales de prueba.
- Generar SQL consistente con los estándares del equipo, de forma automática.
- Impedir la ejecución accidental de operaciones destructivas sobre la base de datos.
- Delegar el análisis a un agente especializado sin saturar el contexto de la conversación principal.
- Compartir toda la configuración del equipo a través de un repositorio en GitHub, lista para que cualquier participante la clone y la use.
