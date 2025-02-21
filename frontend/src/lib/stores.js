import { writable } from "svelte/store";

export const toasts = writable([]);

export const authenticated = writable(false);

export const addToast = (toast) => {
  // Create a unique ID so we can easily find/remove it
  // if it is dismissible/has a timeout.
  const id = Math.floor(Math.random() * 10000);
  const timeout = 5000

  // Setup some sensible defaults for a toast.
  const defaults = {
    id,
    type: "info",
    message: "dies ist ein Toast",
    heading: "Benachrichtigung"
  };

  // Push the toast to the top of the list of toasts
  toasts.update((all) => [{ ...defaults, ...toast }, ...all]);

  // If toast is dismissible, dismiss it after "timeout" amount of time.
  setTimeout(() => dismissToast(id), timeout);
};

export const dismissToast = (id) => {
  toasts.update((all) => all.filter((t) => t.id !== id));
};