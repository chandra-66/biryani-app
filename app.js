const dishes = [
  {
    id: "nawabi-chicken", name: "Nawabi Chicken Dum", restaurant: "The Nawaab's Table",
    category: "Chicken", price: 229, rating: "4.9", tag: "BESTSELLER", spice: "Medium",
    image: "https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?auto=format&fit=crop&w=720&q=82",
    description: "Tender chicken, saffron basmati, and the kind of slow-cooked masala you remember."
  },
  {
    id: "old-city-mutton", name: "Old City Mutton", restaurant: "The Nawaab's Table",
    category: "Mutton", price: 289, rating: "4.8", tag: "SLOW COOKED", spice: "Hot",
    image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=720&q=82",
    description: "Fall-apart mutton, whole spices, and fragrant rice sealed in a traditional handi."
  },
  {
    id: "garden-handi", name: "Garden Handi Biryani", restaurant: "Saffron & Stories",
    category: "Veg", price: 199, rating: "4.7", tag: "GARDEN FRESH", spice: "Mild",
    image: "https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=720&q=82",
    description: "Seasonal vegetables, bright herbs, and delicate dum rice for a happier kind of veg."
  },
  {
    id: "kebab-chicken", name: "Kebab House Special", restaurant: "Dum & Done",
    category: "Special", price: 249, rating: "4.9", tag: "HOUSE SPECIAL", spice: "Medium",
    image: "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=720&q=82",
    description: "Smoky charred kebabs tucked into buttery rice, with a little Kolkata-style magic."
  },
  {
    id: "pepper-chicken", name: "Pepper Chicken Dum", restaurant: "Saffron & Stories",
    category: "Chicken", price: 239, rating: "4.8", tag: "A LITTLE KICK", spice: "Hot",
    image: "https://images.unsplash.com/photo-1599043513900-ed6fe01d3833?auto=format&fit=crop&w=720&q=82",
    description: "Black pepper warmth, juicy chicken, and a slow-cooked finish that lingers."
  },
  {
    id: "paneer-dum", name: "Paneer Saffron Pot", restaurant: "Dum & Done",
    category: "Veg", price: 209, rating: "4.6", tag: "VEG FAVORITE", spice: "Mild",
    image: "https://images.unsplash.com/photo-1567337710282-00832b415979?auto=format&fit=crop&w=720&q=82",
    description: "Golden saffron rice, soft paneer, and a lovely little crunch of fried onions."
  },
  {
    id: "royal-mutton", name: "Royal Mutton Kacchi", restaurant: "Saffron & Stories",
    category: "Mutton", price: 319, rating: "4.9", tag: "WEEKEND FAVORITE", spice: "Medium",
    image: "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=720&q=82",
    description: "A weekend-worthy kacchi with marinated mutton, mint, and tender rice."
  },
  {
    id: "dum-aloo", name: "Kashmiri Dum Aloo Pot", restaurant: "The Nawaab's Table",
    category: "Special", price: 219, rating: "4.7", tag: "SOMETHING NEW", spice: "Mild",
    image: "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?auto=format&fit=crop&w=720&q=82",
    description: "Baby potatoes, warm Kashmiri spices, and a gentle, fragrant dum."
  }
];

const ORDER_STORAGE_KEY = "dum.restaurant.orders";

const state = {
  category: "All",
  vegetarianOnly: false,
  search: "",
  sortByRating: false,
  cart: new Map(),
  favorites: new Set(),
  lastOrder: null
};

const dishGrid = document.querySelector("#dish-grid");
const emptyState = document.querySelector("#empty-state");
const searchInput = document.querySelector("#dish-search");
const suggestions = document.querySelector("#search-suggestions");
const toast = document.querySelector("#toast");
let toastTimer;

function renderDishes() {
  let visible = dishes.filter((dish) => {
    const matchesCategory = state.category === "All"
      || (state.category === "Chicken" && dish.category === "Chicken")
      || (state.category === "Mutton" && dish.category === "Mutton")
      || (state.category === "Veg" && dish.category === "Veg")
      || (state.category === "Special" && dish.category === "Special");
    const matchesDiet = !state.vegetarianOnly || dish.category === "Veg";
    const query = state.search.trim().toLowerCase();
    const matchesSearch = !query || `${dish.name} ${dish.restaurant} ${dish.category}`.toLowerCase().includes(query);
    return matchesCategory && matchesDiet && matchesSearch;
  });
  if (state.sortByRating) visible = [...visible].sort((a, b) => Number(b.rating) - Number(a.rating));

  dishGrid.innerHTML = visible.map((dish) => `
    <article class="dish-card">
      <div class="dish-photo">
        <img src="${dish.image}" alt="${dish.name}, served fresh from ${dish.restaurant}" loading="lazy" />
        <span class="dish-tag ${dish.tag === "BESTSELLER" ? "bestseller" : ""}">${dish.tag}</span>
        <button class="favorite-button" data-favorite="${dish.id}" type="button" aria-label="${state.favorites.has(dish.id) ? "Remove" : "Add"} ${dish.name} ${state.favorites.has(dish.id) ? "from" : "to"} favorites" aria-pressed="${state.favorites.has(dish.id)}">${state.favorites.has(dish.id) ? "♥" : "♡"}</button>
      </div>
      <div class="dish-content">
        <div class="dish-title-row"><h3>${dish.name}</h3><span class="dish-rating">★ ${dish.rating}</span></div>
        <p class="dish-restaurant">${dish.restaurant} · ${dish.spice}</p>
        <div class="dish-bottom"><span class="dish-price">₹${dish.price}<small>/ portion</small></span><button class="add-button" data-add="${dish.id}" type="button" aria-label="Add ${dish.name} to bag">+</button></div>
      </div>
    </article>
  `).join("");
  emptyState.hidden = visible.length > 0;
  dishGrid.hidden = visible.length === 0;
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2600);
}

function addToCart(id) {
  const dish = dishes.find((item) => item.id === id);
  if (!dish) return;
  const current = state.cart.get(id);
  state.cart.set(id, { dish, quantity: current ? current.quantity + 1 : 1 });
  renderCart();
  showToast(`${dish.name} added to your bag`);
}

function renderCart() {
  const count = [...state.cart.values()].reduce((sum, item) => sum + item.quantity, 0);
  const total = [...state.cart.values()].reduce((sum, item) => sum + item.dish.price * item.quantity, 0);
  const cartFooter = document.querySelector("#cart-footer");
  document.querySelector("#cart-count").textContent = String(count);
  document.querySelector("#cart-open").setAttribute("aria-label", `Open shopping bag, ${count} ${count === 1 ? "item" : "items"}`);
  document.querySelector("#drawer-count").textContent = `(${count})`;
  document.querySelector("#cart-subtotal").textContent = `₹${total}`;
  cartFooter.hidden = count === 0;
  const content = document.querySelector("#cart-content");
  if (count === 0) {
    if (state.lastOrder) {
      content.innerHTML = `
        <section class="order-confirmation" aria-labelledby="order-confirmation-title">
          <span class="order-confirmation-icon" aria-hidden="true">✓</span>
          <h3 id="order-confirmation-title">Your order is placed!</h3>
          <p class="order-confirmation-note">Here are the delivery details for your order.</p>
          <dl class="order-customer-details">
            <div><dt>Customer name</dt><dd data-order-name></dd></div>
            <div><dt>Phone number</dt><dd data-order-phone></dd></div>
            <div><dt>Delivery address</dt><dd data-order-address></dd></div>
          </dl>
          <h4>Items ordered</h4>
          <ul class="order-items" data-order-items></ul>
          <div class="order-total"><span>Total</span><strong data-order-total></strong></div>
          <button class="button button-outline" data-close-drawer type="button">Continue browsing</button>
        </section>`;
      content.querySelector("[data-order-name]").textContent = state.lastOrder.name;
      content.querySelector("[data-order-phone]").textContent = state.lastOrder.phone;
      content.querySelector("[data-order-address]").textContent = state.lastOrder.address;
      content.querySelector("[data-order-total]").textContent = `₹${state.lastOrder.total}`;
      const orderItems = content.querySelector("[data-order-items]");
      state.lastOrder.items.forEach((item) => {
        const row = document.createElement("li");
        row.textContent = `${item.name} × ${item.quantity} — ₹${item.price * item.quantity}`;
        orderItems.append(row);
      });
      return;
    }
    content.innerHTML = `<div class="empty-cart"><span>🍚</span><h3>Your bag's a little empty.</h3><p>Somewhere out there, a very good biryani is waiting for you.</p><button class="button button-outline" data-close-drawer type="button">Let's find it</button></div>`;
    return;
  }
  content.innerHTML = [...state.cart.entries()].map(([id, item]) => `
    <article class="cart-item">
      <img src="${item.dish.image}" alt="" />
      <div><h3>${item.dish.name}</h3><small>${item.dish.restaurant}</small><div class="quantity-control"><button data-quantity="${id}" data-change="-1" type="button" aria-label="Remove one ${item.dish.name}">−</button><span>${item.quantity}</span><button data-quantity="${id}" data-change="1" type="button" aria-label="Add one ${item.dish.name}">+</button></div></div>
      <span class="cart-item-price">₹${item.dish.price * item.quantity}</span>
    </article>
  `).join("");
}

function setOverlay(open) {
  const overlay = document.querySelector("#overlay");
  overlay.hidden = !open;
  document.body.classList.toggle("no-scroll", open);
  requestAnimationFrame(() => overlay.classList.toggle("visible", open));
}

function openCart() {
  document.querySelector("#assistant-panel").classList.remove("open");
  document.querySelector("#cart-drawer").classList.add("open");
  document.querySelector("#cart-drawer").setAttribute("aria-hidden", "false");
  setOverlay(true);
  document.querySelector("#cart-open").setAttribute("aria-expanded", "true");
  document.querySelector("[data-close-drawer]")?.focus();
}

function closeCart() {
  document.querySelector("#cart-drawer").classList.remove("open");
  document.querySelector("#cart-drawer").setAttribute("aria-hidden", "true");
  document.querySelector("#cart-open").setAttribute("aria-expanded", "false");
  if (!document.querySelector("#assistant-panel").classList.contains("open")) setOverlay(false);
  document.querySelector("#cart-open").focus();
}

function toggleFavorite(id) {
  const button = document.querySelector(`[data-favorite="${id}"]`);
  const restaurantButton = button?.classList.contains("restaurant-heart");
  if (state.favorites.has(id)) {
    state.favorites.delete(id);
    showToast("Removed from your favorites");
  } else {
    state.favorites.add(id);
    showToast("Saved for your next craving");
  }
  if (restaurantButton) {
    button.setAttribute("aria-pressed", String(state.favorites.has(id)));
    button.textContent = state.favorites.has(id) ? "♥" : "♡";
  } else {
    renderDishes();
  }
}

function handleSearch(value) {
  state.search = value;
  renderDishes();
  const query = value.trim().toLowerCase();
  if (!query) {
    suggestions.classList.remove("open");
    suggestions.replaceChildren();
    return;
  }
  const matches = dishes.filter((dish) => `${dish.name} ${dish.restaurant}`.toLowerCase().includes(query)).slice(0, 4);
  suggestions.innerHTML = matches.map((dish) => `<button class="search-suggestion" type="button" role="option" data-suggestion="${dish.name}"><span>${dish.name}</span><small>${dish.restaurant}</small></button>`).join("");
  suggestions.classList.toggle("open", matches.length > 0);
}

function openAssistant() {
  document.querySelector("#cart-drawer").classList.remove("open");
  document.querySelector("#cart-drawer").setAttribute("aria-hidden", "true");
  const panel = document.querySelector("#assistant-panel");
  panel.classList.add("open");
  panel.setAttribute("aria-hidden", "false");
  setOverlay(false);
  document.querySelector("#chat-input").focus();
}

function recommend(query) {
  const normalized = query.toLowerCase();
  let matches = dishes.filter((dish) => {
    const vegetarianMatch = /\b(veg|vegetarian|paneer)\b/.test(normalized) ? dish.category === "Veg" : true;
    const chickenMatch = /\b(chicken)\b/.test(normalized) ? dish.category === "Chicken" : true;
    const muttonMatch = /\b(mutton)\b/.test(normalized) ? dish.category === "Mutton" : true;
    const spicyMatch = /\b(spicy|hot)\b/.test(normalized) ? dish.spice === "Hot" : true;
    const underMatch = normalized.match(/(?:under|below|less than)\s*₹?\s*(\d+)/);
    const budgetMatch = !underMatch || dish.price < Number(underMatch[1]);
    return vegetarianMatch && chickenMatch && muttonMatch && spicyMatch && budgetMatch;
  });
  if (!matches.length) matches = [...dishes].sort((a, b) => Number(b.rating) - Number(a.rating)).slice(0, 2);
  return matches.slice(0, 2);
}

document.querySelector("#category-grid").addEventListener("click", (event) => {
  const button = event.target.closest("[data-category]");
  if (!button) return;
  state.category = button.dataset.category;
  document.querySelectorAll(".category-card").forEach((card) => card.classList.toggle("selected", card === button));
  renderDishes();
  document.querySelector("#dishes").scrollIntoView({ behavior: "smooth", block: "start" });
});

document.querySelector("#dish-grid").addEventListener("click", (event) => {
  const addButton = event.target.closest("[data-add]");
  const favoriteButton = event.target.closest("[data-favorite]");
  if (addButton) addToCart(addButton.dataset.add);
  if (favoriteButton) toggleFavorite(favoriteButton.dataset.favorite);
});

document.querySelector("#veg-filter").addEventListener("change", (event) => {
  state.vegetarianOnly = event.target.checked;
  renderDishes();
});

document.querySelector("#sort-button").addEventListener("click", (event) => {
  state.sortByRating = !state.sortByRating;
  event.currentTarget.innerHTML = state.sortByRating ? 'Top rated <span aria-hidden="true">⌄</span>' : 'Popular <span aria-hidden="true">⌄</span>';
  renderDishes();
});

searchInput.addEventListener("input", (event) => handleSearch(event.target.value));
document.querySelector("#search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  state.search = searchInput.value.trim();
  suggestions.classList.remove("open");
  renderDishes();
  document.querySelector("#dishes").scrollIntoView({ behavior: "smooth" });
});
suggestions.addEventListener("click", (event) => {
  const choice = event.target.closest("[data-suggestion]");
  if (!choice) return;
  searchInput.value = choice.dataset.suggestion;
  handleSearch(choice.dataset.suggestion);
  suggestions.classList.remove("open");
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-bar")) suggestions.classList.remove("open");
});
document.querySelector("#clear-filters").addEventListener("click", () => {
  state.search = "";
  state.category = "All";
  state.vegetarianOnly = false;
  searchInput.value = "";
  document.querySelector("#veg-filter").checked = false;
  document.querySelectorAll(".category-card").forEach((card) => card.classList.toggle("selected", card.dataset.category === "All"));
  renderDishes();
});

document.querySelector("#cart-open").addEventListener("click", openCart);
document.querySelector("#overlay").addEventListener("click", closeCart);
document.querySelector("#cart-drawer").addEventListener("click", (event) => {
  const closeButton = event.target.closest("[data-close-drawer]");
  const quantityButton = event.target.closest("[data-quantity]");
  if (closeButton) closeCart();
  if (quantityButton) {
    const id = quantityButton.dataset.quantity;
    const item = state.cart.get(id);
    if (!item) return;
    item.quantity += Number(quantityButton.dataset.change);
    if (item.quantity <= 0) state.cart.delete(id);
    renderCart();
  }
});
document.querySelector("#checkout-button").addEventListener("click", () => {
  const count = [...state.cart.values()].reduce((sum, item) => sum + item.quantity, 0);
  if (count === 0) {
    showToast("Add a few biryanis to your bag first.");
    return;
  }
  document.querySelector("#checkout-button").hidden = true;
  document.querySelector("#checkout-form").hidden = false;
  document.querySelector("#customer-name").focus();
});
document.querySelector("#checkout-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!event.currentTarget.reportValidity()) return;

  const items = [...state.cart.values()].map(({ dish, quantity }) => ({
    name: dish.name,
    price: dish.price,
    quantity
  }));
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const order = {
    id: `DUM-${Date.now()}`,
    name: document.querySelector("#customer-name").value.trim(),
    phone: document.querySelector("#customer-phone").value.trim(),
    address: document.querySelector("#delivery-address").value.trim(),
    items,
    total,
    status: "new"
  };
  let orders;
  try {
    const savedOrders = localStorage.getItem(ORDER_STORAGE_KEY);
    orders = savedOrders ? JSON.parse(savedOrders) : [];
    if (!Array.isArray(orders)) throw new Error("Saved orders must be an array.");
    localStorage.setItem(ORDER_STORAGE_KEY, JSON.stringify([...orders, order]));
  } catch (error) {
    console.error("Could not save the order for the restaurant.", error);
    showToast("Could not send your order to the restaurant. Please try again.");
    return;
  }
  state.lastOrder = order;
  state.cart.clear();
  document.querySelector("#checkout-form").reset();
  document.querySelector("#checkout-form").hidden = true;
  document.querySelector("#checkout-button").hidden = false;
  renderCart();
  showToast("Order placed and sent to the restaurant.");
});
document.querySelector("#show-more").addEventListener("click", () => {
  state.category = "All";
  state.search = "";
  state.vegetarianOnly = false;
  searchInput.value = "";
  document.querySelector("#veg-filter").checked = false;
  document.querySelectorAll(".category-card").forEach((card) => card.classList.toggle("selected", card.dataset.category === "All"));
  renderDishes();
  document.querySelector("#show-more").textContent = "That's the whole pot — made with love.";
});
document.querySelectorAll(".restaurant-heart").forEach((button, index) => {
  button.dataset.favorite = `restaurant-${index}`;
  button.addEventListener("click", () => toggleFavorite(button.dataset.favorite));
});
document.querySelectorAll(".promo-cta").forEach((button) => button.addEventListener("click", () => showToast(`Code ${button.dataset.coupon} copied — enjoy ₹100 off!`)));

document.querySelector("#theme-toggle").addEventListener("click", (event) => {
  const dark = document.body.classList.toggle("dark-mode");
  event.currentTarget.setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} mode`);
});
document.querySelector("#menu-toggle").addEventListener("click", (event) => {
  const nav = document.querySelector("#mobile-nav");
  const open = nav.classList.toggle("open");
  event.currentTarget.setAttribute("aria-expanded", String(open));
  event.currentTarget.setAttribute("aria-label", open ? "Close navigation menu" : "Open navigation menu");
});
document.querySelectorAll("#mobile-nav a").forEach((link) => link.addEventListener("click", () => {
  document.querySelector("#mobile-nav").classList.remove("open");
  document.querySelector("#menu-toggle").setAttribute("aria-expanded", "false");
}));
document.querySelector("#assistant-open").addEventListener("click", openAssistant);
document.querySelector("#assistant-close").addEventListener("click", () => {
  document.querySelector("#assistant-panel").classList.remove("open");
  document.querySelector("#assistant-panel").setAttribute("aria-hidden", "true");
});
document.querySelector("#chat-messages").addEventListener("click", (event) => {
  const prompt = event.target.closest(".suggested-prompts button");
  const addButton = event.target.closest("[data-chat-add]");
  if (prompt) sendChat(prompt.textContent);
  if (addButton) addToCart(addButton.dataset.chatAdd);
});
function sendChat(message) {
  const chat = document.querySelector("#chat-messages");
  const userBubble = document.createElement("div");
  userBubble.className = "chat-bubble user-bubble";
  userBubble.textContent = message;
  chat.append(userBubble);
  document.querySelector(".suggested-prompts")?.remove();
  const reply = document.createElement("div");
  reply.className = "chat-bubble assistant-bubble";
  reply.textContent = "Let me find a good match for you…";
  chat.append(reply);
  chat.scrollTop = chat.scrollHeight;
  window.setTimeout(() => {
    const found = recommend(message);
    reply.textContent = found.length ? "This one sounds like your kind of thing:" : "I couldn't find an exact match, but these are local favorites:";
    const cards = document.createElement("div");
    cards.innerHTML = found.map((dish) => `<article class="chat-recommendation"><img src="${dish.image}" alt="" /><div><strong>${dish.name}</strong><small>₹${dish.price} · ★ ${dish.rating}</small></div><button type="button" data-chat-add="${dish.id}" aria-label="Add ${dish.name} to bag">+</button></article>`).join("");
    chat.append(cards);
    chat.scrollTop = chat.scrollHeight;
  }, 450);
}
document.querySelector("#chat-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.querySelector("#chat-input");
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  sendChat(message);
});
document.querySelector("#newsletter-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const email = document.querySelector("#newsletter-email");
  if (!email.checkValidity()) {
    email.reportValidity();
    return;
  }
  showToast("You’re on the list. Good things are on their way!");
  event.currentTarget.reset();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    if (document.querySelector("#cart-drawer").classList.contains("open")) closeCart();
    document.querySelector("#assistant-panel").classList.remove("open");
    document.querySelector("#assistant-panel").setAttribute("aria-hidden", "true");
    document.querySelector("#mobile-nav").classList.remove("open");
    document.querySelector("#menu-toggle").setAttribute("aria-expanded", "false");
  }
});

renderDishes();
renderCart();
