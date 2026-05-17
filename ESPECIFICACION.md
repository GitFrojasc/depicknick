# dePicknick — Especificación del Proyecto

## Visión
Franquicia tecnológica de mercados campesinos. El sistema conoce profundamente cada producto y lo vende a escala mediante agentes IA.

Pereira es el piloto. Cuando funcione aquí, se replica.

---

## Modelo de negocio

### Logística
| Tipo | Quién envía | Ejemplo |
|------|-------------|---------|
| Centro de acopio | El acopiador | Canastos armados, combos |
| Envío directo | El productor | Queso específico, café especial |

### El bot es el vendedor
- Conoce todo el catálogo con historia profunda
- Argumenta, recomienda, cierra la venta
- Atiende 24/7

### Modelo editorial
- Productores entregan material crudo
- dePicknick edita y produce el contenido
- Los videos sirven para YouTube Y para la tienda

---

## Estructura multi-mercado

```
dePicknick (plataforma)
├── Mercado Pereira      → acopiador: Francisco
├── Mercado Manizales    → acopiador: por definir
└── Mercado Medellín     → acopiador: por definir
```

**La plataforma aporta:** tecnología, editorial, estándares, agente IA
**El acopiador aporta:** productores locales, acopio físico, envíos, territorio

---

## Módulo Productor (arquitectura nueva)

### Estados editoriales
```
borrador → en_revision → publicado → destacado
```

### Tipo de acuerdo
- `acopio` — el acopiador maneja el stock
- `directo` — el productor envía al cliente
- `ambos` — depende del producto

### Requisitos mínimos para publicar
**Obligatorio**
- Foto del productor (en finca o con su producto)
- Foto de cada producto
- Historia del productor (mínimo 3 líneas)
- Descripción de cada producto
- Precios actualizados
- Teléfono y email activos

**Recomendado**
- Video (YouTube, TikTok, o producido por dePicknick)
- Historia de cada producto
- Certificaciones
- Temporadas de disponibilidad

### Puntaje de completitud
Visible en admin. Perfil 100% = más visibilidad en la tienda.

---

## Agentes IA

| Agente | Función |
|--------|---------|
| Auditor | Detecta información faltante en productos/productores |
| Contacto | Pregunta a productores por email/WhatsApp, envía Excel |
| Asistente | Atiende clientes, vende y argumenta en la tienda |

### Capas de conocimiento
1. **DB estructurada** — productos, precios, stock
2. **DocumentoRAG / Wiki** — historia profunda, temporadas, variedades
3. **Conversaciones** — historial Q&A, el sistema aprende

### Tech
- Google Gemini (AI Studio, 90 días disponibles)
- Sin vectores en el prototipo — contexto grande de Gemini
- pgvector cuando el catálogo crezca

---

## Roadmap

- [ ] Resolver Google OAuth
- [ ] Reconstruir módulo Productor (estados + acuerdos + multi-mercado)
- [ ] Ingresar productor de prueba, flujo editorial completo
- [ ] Agente Asistente funcionando (Gemini + RAG)
- [ ] Demo público en Pereira
- [ ] Multi-mercado (segundo acopiador)
