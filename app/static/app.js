let ticketSeleccionado = null;
let ticketTituloSeleccionado = null;
const PASOS_WORKFLOW = ["Clasificación", "Búsqueda de conocimiento", "Redacción", "Supervisión"];

async function api(path, options = {}) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function setEstado(texto, tipo = "idle") {
  const status = document.getElementById("workflowStatus");
  status.textContent = texto;
  status.className = `status status-${tipo}`;
}

function renderPasos(pasos = [], pasoActivo = -1) {
  const cont = document.getElementById("workflowSteps");
  cont.innerHTML = "";
  const base = pasos.length ? pasos : PASOS_WORKFLOW;

  for (let i = 0; i < base.length; i += 1) {
    const paso = base[i];
    const nombre = typeof paso === "string" ? paso : (paso?.nombre || `Paso ${i + 1}`);
    const detalle = typeof paso === "string" ? "" : (paso?.detalle || "");
    const estado = typeof paso === "string" ? null : paso?.estado;

    const li = document.createElement("li");
    li.className = "step";
    li.innerHTML = `
      <strong>${nombre}</strong>
      ${detalle ? `<span class="step-detail">${detalle}</span>` : ""}
    `;
    if (i < pasoActivo) li.classList.add("step-done");
    if (i === pasoActivo) li.classList.add("step-active");
    if (estado === "fallback") li.classList.add("step-fallback");
    cont.appendChild(li);
  }
}

function renderRespuestaAgente(result) {
  document.getElementById("respuestaEmpty").textContent = "Resultado más reciente:";

  document.getElementById("metaClasificacion").textContent = `Clasificación: ${result.clasificacion || "-"}`;
  document.getElementById("metaModo").textContent = `Modo: ${result.modo || "-"}`;
  document.getElementById("metaProveedor").textContent = `Proveedor: ${result.proveedor || "-"}`;
  const articulos = Array.isArray(result.articulos_usados) ? result.articulos_usados.join(", ") : "-";
  document.getElementById("metaArticulos").textContent = `Artículos: ${articulos || "-"}`;

  const escalamiento = document.getElementById("metaEscalamiento");
  escalamiento.textContent = `Escalamiento: ${result.requiere_escalamiento ? "Sí" : "No"}`;
  escalamiento.className = `pill ${result.requiere_escalamiento ? "pill-warn" : "pill-ok"}`;

  document.getElementById("respuestaTexto").textContent = result.respuesta_sugerida || "Sin respuesta sugerida.";
  document.getElementById("respuestaRazon").textContent = result.razon_escalamiento || "Sin detalle de supervisión.";
}

function resetRespuestaAgente() {
  document.getElementById("respuestaEmpty").textContent = "La respuesta del agente aparecerá aquí después de ejecutar el workflow.";
  document.getElementById("metaClasificacion").textContent = "Clasificación: -";
  document.getElementById("metaEscalamiento").textContent = "Escalamiento: -";
  document.getElementById("metaEscalamiento").className = "pill";
  document.getElementById("metaModo").textContent = "Modo: -";
  document.getElementById("metaProveedor").textContent = "Proveedor: -";
  document.getElementById("metaArticulos").textContent = "Artículos: -";
  document.getElementById("respuestaTexto").textContent = "Sin ejecución todavía.";
  document.getElementById("respuestaRazon").textContent = "Sin ejecución todavía.";
}

async function cargarTickets() {
  const ul = document.getElementById("tickets");
  ul.innerHTML = "<li class='list-item'>Cargando tickets...</li>";
  const tickets = await api("/api/tickets");
  ul.innerHTML = "";
  for (const t of tickets) {
    const li = document.createElement("li");
    li.className = "list-item";
    if (t.id === ticketSeleccionado) li.classList.add("ticket-selected");

    const titulo = document.createElement("p");
    titulo.className = "list-item-title";
    titulo.textContent = `#${t.id} - ${t.titulo}`;

    const meta = document.createElement("p");
    meta.className = "list-item-meta";
    meta.textContent = `Curso: ${t.curso}`;

    const acciones = document.createElement("div");
    acciones.className = "ticket-actions";

    const btn = document.createElement("button");
    btn.className = "btn";
    btn.textContent = `Seleccionar #${t.id}`;
    btn.onclick = () => seleccionarTicket(t.id, t.titulo);
    acciones.appendChild(btn);
    li.appendChild(titulo);
    li.appendChild(meta);
    li.appendChild(acciones);
    ul.appendChild(li);
  }
}

async function cargarArticulos() {
  const ul = document.getElementById("articulos");
  ul.innerHTML = "<li class='list-item'>Cargando artículos...</li>";
  const articulos = await api("/api/articulos");
  ul.innerHTML = "";
  for (const a of articulos) {
    const li = document.createElement("li");
    li.className = "list-item";
    li.innerHTML = `
      <p class="list-item-title">#${a.id} - ${a.titulo}</p>
      <p class="list-item-meta">Categoría: ${a.categoria}</p>
    `;
    ul.appendChild(li);
  }
}

async function cargarHistorial(ticketId) {
  const hint = document.getElementById("historialHint");
  hint.textContent = `Ticket #${ticketId}`;
  const historial = await api(`/api/tickets/${ticketId}/ejecuciones`);
  const ul = document.getElementById("historial");
  ul.innerHTML = "";
  if (!historial.length) {
    ul.innerHTML = "<li class='list-item'>Aún no hay ejecuciones para este ticket.</li>";
    return;
  }
  for (const h of historial) {
    const li = document.createElement("li");
    li.className = "list-item";
    li.innerHTML = `
      <p class="list-item-title">Ejecución #${h.id}</p>
      <p class="list-item-meta">Clasificación: ${h.clasificacion}</p>
      <p class="list-item-meta">Escalamiento: ${h.requiere_escalamiento ? "Sí" : "No"}</p>
    `;
    ul.appendChild(li);
  }
}

function seleccionarTicket(id, titulo) {
  ticketSeleccionado = id;
  ticketTituloSeleccionado = titulo;
  setEstado(`Ticket seleccionado: #${id} - ${titulo}`, "idle");
  renderPasos();
  document.getElementById("runWorkflow").disabled = false;
  document.getElementById("resultado").textContent = "";
  resetRespuestaAgente();
  cargarHistorial(id);
  cargarTickets();
}

async function ejecutarWorkflow() {
  if (!ticketSeleccionado) return;
  const out = document.getElementById("resultado");
  setEstado("Ejecutando agentes del workflow...", "running");
  renderPasos(PASOS_WORKFLOW, 0);
  out.textContent = "";

  for (let i = 0; i < PASOS_WORKFLOW.length; i += 1) {
    renderPasos(PASOS_WORKFLOW, i);
    await new Promise((resolve) => setTimeout(resolve, 160));
  }

  try {
    const result = await api(`/api/workflow/ejecutar/${ticketSeleccionado}`, { method: "POST" });
    renderRespuestaAgente(result);
    out.textContent = JSON.stringify(result, null, 2);
    const pasos = Array.isArray(result.pasos) && result.pasos.length ? result.pasos : PASOS_WORKFLOW;
    renderPasos(pasos, pasos.length);
    setEstado(`Workflow completado para ticket #${ticketSeleccionado} - ${ticketTituloSeleccionado}.`, "ok");
    await cargarHistorial(ticketSeleccionado);
  } catch (e) {
    setEstado(`Error: ${e.message}`, "error");
    renderPasos(PASOS_WORKFLOW, -1);
  }
}

document.getElementById("refreshTickets").onclick = cargarTickets;
document.getElementById("refreshArticulos").onclick = cargarArticulos;
document.getElementById("runWorkflow").onclick = ejecutarWorkflow;

setEstado("Seleccione un ticket para ejecutar.", "idle");
renderPasos();
resetRespuestaAgente();
cargarTickets();
cargarArticulos();
