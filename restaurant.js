const ORDER_STORAGE_KEY = "dum.restaurant.orders";
const state = { orders: [] };
const labels = {
  new: "New",
  accepted: "Accepted",
  preparing: "Preparing",
  ready: "Ready for pickup",
  completed: "Completed",
  rejected: "Rejected"
};
let toastTimer;

function readOrders() {
  const savedOrders = localStorage.getItem(ORDER_STORAGE_KEY);
  if (!savedOrders) return [];

  const orders = JSON.parse(savedOrders);
  if (!Array.isArray(orders)) throw new Error("Saved orders must be an array.");
  if (orders.some((order) => !order || typeof order.id !== "string" || !Array.isArray(order.items) || !labels[order.status])) {
    throw new Error("Saved order data is invalid.");
  }
  return orders;
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2800);
}

function setDashboardError(message) {
  const error = document.querySelector("#dashboard-error");
  error.textContent = message;
  error.hidden = !message;
}

function renderOrderCard(order) {
  const card = document.createElement("article");
  card.className = "dashboard-order";

  const header = document.createElement("div");
  header.className = "dashboard-order-header";
  const title = document.createElement("div");
  const heading = document.createElement("h3");
  heading.textContent = `Order ${order.id}`;
  const customerName = document.createElement("p");
  customerName.textContent = `Customer: ${order.name}`;
  title.append(heading, customerName);

  const status = document.createElement("span");
  status.className = `order-status status-${order.status}`;
  status.textContent = labels[order.status];
  header.append(title, status);
  card.append(header);

  const details = document.createElement("div");
  details.className = "dashboard-customer";
  [
    ["Phone number", order.phone],
    ["Delivery address", order.address]
  ].forEach(([label, value]) => {
    const line = document.createElement("p");
    const name = document.createElement("strong");
    name.textContent = `${label}: `;
    line.append(name, document.createTextNode(value));
    details.append(line);
  });
  card.append(details);

  const items = document.createElement("ul");
  items.className = "dashboard-order-items";
  order.items.forEach((item) => {
    const line = document.createElement("li");
    line.textContent = `${item.name} × ${item.quantity} — ₹${item.price * item.quantity}`;
    items.append(line);
  });
  card.append(items);

  const footer = document.createElement("div");
  footer.className = "dashboard-order-footer";
  const total = document.createElement("strong");
  total.textContent = `Total: ₹${order.total}`;
  footer.append(total);

  const actions = document.createElement("div");
  actions.className = "dashboard-order-actions";
  if (order.status === "new") {
    actions.append(
      createOrderAction("Accept", "accepted", order.id, "button-primary"),
      createOrderAction("Reject", "rejected", order.id, "button-outline")
    );
  } else if (order.status === "accepted") {
    actions.append(createOrderAction("Start preparation", "preparing", order.id, "button-primary"));
  } else if (order.status === "preparing") {
    actions.append(createOrderAction("Mark ready", "ready", order.id, "button-primary"));
  } else if (order.status === "ready") {
    actions.append(createOrderAction("Complete order", "completed", order.id, "button-primary"));
  }
  footer.append(actions);
  card.append(footer);
  return card;
}

function createOrderAction(label, status, orderId, style) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `button ${style}`;
  button.textContent = label;
  button.dataset.orderAction = status;
  button.dataset.orderId = orderId;
  return button;
}

function renderNotifications() {
  const newOrders = state.orders.filter((order) => order.status === "new");
  const count = document.querySelector("#notification-count");
  count.hidden = newOrders.length === 0;
  count.textContent = String(newOrders.length);
  document.querySelector("#notifications-toggle").setAttribute(
    "aria-label",
    `New order notifications, ${newOrders.length} new ${newOrders.length === 1 ? "order" : "orders"}`
  );

  const list = document.querySelector("#notification-list");
  list.replaceChildren();
  if (newOrders.length === 0) {
    const empty = document.createElement("p");
    empty.className = "notification-empty";
    empty.textContent = "No new orders. New orders from customers will appear here.";
    list.append(empty);
    return;
  }

  newOrders.slice().reverse().forEach((order) => {
    const notice = document.createElement("article");
    notice.className = "order-notification";
    const heading = document.createElement("h3");
    heading.textContent = `New order from ${order.name}`;
    const phone = document.createElement("p");
    phone.textContent = `Phone: ${order.phone}`;
    const address = document.createElement("p");
    address.textContent = `Delivery address: ${order.address}`;
    const items = document.createElement("ul");
    order.items.forEach((item) => {
      const line = document.createElement("li");
      line.textContent = `${item.name} × ${item.quantity}`;
      items.append(line);
    });
    const total = document.createElement("p");
    total.className = "notification-total";
    total.textContent = `Order total: ₹${order.total}`;
    const viewOrder = document.createElement("a");
    viewOrder.className = "button button-primary";
    viewOrder.href = "#order-queue";
    viewOrder.textContent = "Review order";
    notice.append(heading, phone, address, items, total, viewOrder);
    list.append(notice);
  });
}

function renderDashboard() {
  const orders = state.orders;
  const filter = document.querySelector("#order-status-filter").value;
  document.querySelector("#new-order-count").textContent = String(
    orders.filter((order) => order.status === "new").length
  );
  document.querySelector("#preparation-order-count").textContent = String(
    orders.filter((order) => ["accepted", "preparing", "ready"].includes(order.status)).length
  );
  document.querySelector("#completed-order-count").textContent = String(
    orders.filter((order) => order.status === "completed").length
  );

  const visibleOrders = orders.filter((order) => {
    if (filter === "active") return !["completed", "rejected"].includes(order.status);
    if (filter === "preparation") return ["accepted", "preparing", "ready"].includes(order.status);
    if (filter === "all") return true;
    return order.status === filter;
  });
  const container = document.querySelector("#dashboard-orders");
  container.replaceChildren();
  if (visibleOrders.length === 0) {
    const message = document.createElement("p");
    message.className = "dashboard-empty";
    message.textContent = orders.length === 0
      ? "No customer orders yet. New orders will appear here."
      : "There are no orders in this view.";
    container.append(message);
    return;
  }
  visibleOrders.slice().reverse().forEach((order) => container.append(renderOrderCard(order)));
}

function refreshOrders(openNewOrderNotice = false) {
  try {
    state.orders = readOrders();
    setDashboardError("");
    if (openNewOrderNotice && state.orders.some((order) => order.status === "new")) {
      document.querySelector("#order-status-filter").value = "active";
    }
    renderDashboard();
    renderNotifications();
    if (openNewOrderNotice && state.orders.some((order) => order.status === "new")) {
      const panel = document.querySelector("#order-notifications");
      panel.hidden = false;
      document.querySelector("#notifications-toggle").setAttribute("aria-expanded", "true");
    }
  } catch (error) {
    console.error("Could not load restaurant orders.", error);
    setDashboardError("Could not load orders from this browser. Check storage access and reload the dashboard.");
  }
}

document.querySelector("#order-status-filter").addEventListener("change", renderDashboard);
document.querySelector("#dashboard-orders").addEventListener("click", (event) => {
  const button = event.target.closest("[data-order-action]");
  if (!button) return;

  const order = state.orders.find((item) => item.id === button.dataset.orderId);
  if (!order) return;
  const allowedTransitions = {
    new: ["accepted", "rejected"],
    accepted: ["preparing"],
    preparing: ["ready"],
    ready: ["completed"],
    completed: [],
    rejected: []
  };
  const nextStatus = button.dataset.orderAction;
  if (!allowedTransitions[order.status].includes(nextStatus)) return;

  const updatedOrders = state.orders.map((item) =>
    item.id === order.id ? { ...item, status: nextStatus } : item
  );
  try {
    localStorage.setItem(ORDER_STORAGE_KEY, JSON.stringify(updatedOrders));
  } catch (error) {
    console.error("Could not save the restaurant order update.", error);
    showToast("Could not save this update. Please try again.");
    return;
  }
  refreshOrders();
  showToast(`Order ${order.id}: ${labels[nextStatus]}.`);
});

document.querySelector("#notifications-toggle").addEventListener("click", () => {
  const panel = document.querySelector("#order-notifications");
  panel.hidden = !panel.hidden;
  document.querySelector("#notifications-toggle").setAttribute("aria-expanded", String(!panel.hidden));
});
document.querySelector("#notifications-close").addEventListener("click", () => {
  document.querySelector("#order-notifications").hidden = true;
  document.querySelector("#notifications-toggle").setAttribute("aria-expanded", "false");
});
document.querySelector("#notification-list").addEventListener("click", (event) => {
  if (event.target.closest('a[href="#order-queue"]')) {
    document.querySelector("#order-notifications").hidden = true;
    document.querySelector("#notifications-toggle").setAttribute("aria-expanded", "false");
  }
});
window.addEventListener("storage", (event) => {
  if (event.key === ORDER_STORAGE_KEY) refreshOrders(true);
});

refreshOrders(true);
