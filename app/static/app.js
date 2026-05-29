let ticketSeleccionado = null;

async function api(path, options = {}) {
  const res = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function cargarTickets() {
  const tickets = await api("/api/tickets");
  const ul = document.getElementById("tickets");
  ul.innerHTML = "";
  for (const t of tickets) {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.textContent = `Seleccionar #${t.id}`;
    btn.onclick = () => seleccionarTicket(t.id, t.titulo);
    li.textContent = `#${t.id} - ${t.titulo} (${t.curso}) `;
    li.appendChild(btn);
    ul.appendChild(li);
  }
}

async function cargarArticulos() {
  const articulos = await api("/api/articulos");
  const ul = document.getElementById("articulos");
  ul.innerHTML = "";
  for (const a of articulos) {
    const li = document.createElement("li");
    li.textContent = `#${a.id} - ${a.titulo} [${a.categoria}]`;
    ul.appendChild(li);
  }
}

async function cargarHistorial(ticketId) {
  const historial = await api(`/api/tickets/${ticketId}/ejecuciones`);
  const ul = document.getElementById("historial");
  ul.innerHTML = "";
  for (const h of historial) {
    const li = document.createElement("li");
    li.textContent = `Ejecución #${h.id} | Clasificación: ${h.clasificacion} | Escalamiento: ${h.requiere_escalamiento ? "Sí" : "No"}`;
    ul.appendChild(li);
  }
}

function seleccionarTicket(id, titulo) {
  ticketSeleccionado = id;
  document.getElementById("workflowStatus").textContent = `Ticket seleccionado: #${id} - ${titulo}`;
  document.getElementById("runWorkflow").disabled = false;
  cargarHistorial(id);
}

async function ejecutarWorkflow() {
  if (!ticketSeleccionado) return;
  const status = document.getElementById("workflowStatus");
  const out = document.getElementById("resultado");
  status.textContent = "Ejecutando agentes: clasificación -> búsqueda -> redacción -> supervisión...";
  try {
    const result = await api(`/api/workflow/ejecutar/${ticketSeleccionado}`, { method: "POST" });
    out.textContent = JSON.stringify(result, null, 2);
    status.textContent = "Workflow completado.";
    await cargarHistorial(ticketSeleccionado);
  } catch (e) {
    status.textContent = `Error: ${e.message}`;
  }
}

document.getElementById("refreshTickets").onclick = cargarTickets;
document.getElementById("refreshArticulos").onclick = cargarArticulos;
document.getElementById("runWorkflow").onclick = ejecutarWorkflow;

cargarTickets();
cargarArticulos();
