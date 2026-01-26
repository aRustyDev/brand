/**
 * aRustyDev Brand Theme Switcher
 *
 * Usage:
 *   <script src="https://brand.arusty.dev/assets/js/theme-switcher.js"></script>
 *   <script>
 *     // Initialize with a theme (loads CSS if not already present)
 *     BrandTheme.init('forest-night');
 *
 *     // Or init with options
 *     BrandTheme.init({
 *       theme: 'forest-night',
 *       mode: 'dark',           // 'light', 'dark', or 'auto'
 *       persist: true,          // save to localStorage (default: true)
 *       onThemeChange: (theme) => console.log('Theme changed:', theme),
 *       onModeChange: (mode) => console.log('Mode changed:', mode),
 *     });
 *   </script>
 *
 * API:
 *   BrandTheme.theme('twilight')     - Switch theme
 *   BrandTheme.mode('dark')          - Switch mode (light/dark/auto)
 *   BrandTheme.toggle()              - Toggle light/dark
 *   BrandTheme.getTheme()            - Get current theme name
 *   BrandTheme.getMode()             - Get current mode
 *   BrandTheme.themes                - List available themes
 */

(function(global) {
  'use strict';

  const CDN_BASE = 'https://brand.arusty.dev/assets/colors/themes';
  const STORAGE_KEY_THEME = 'brand-theme';
  const STORAGE_KEY_MODE = 'brand-mode';
  const AVAILABLE_THEMES = ['deep-water', 'forest-night', 'twilight'];
  const LINK_ID = 'brand-theme-stylesheet';

  let currentTheme = null;
  let currentMode = null;
  let options = {
    persist: true,
    onThemeChange: null,
    onModeChange: null,
  };

  /**
   * Get or create the theme stylesheet link element
   */
  function getStylesheetLink() {
    let link = document.getElementById(LINK_ID);
    if (!link) {
      // Check if there's an existing brand theme link
      link = document.querySelector(`link[href*="brand.arusty.dev/assets/colors/themes"]`);
      if (link) {
        link.id = LINK_ID;
      } else {
        // Create new link element
        link = document.createElement('link');
        link.id = LINK_ID;
        link.rel = 'stylesheet';
        document.head.appendChild(link);
      }
    }
    return link;
  }

  /**
   * Load a theme CSS file
   */
  function loadTheme(themeName) {
    if (!AVAILABLE_THEMES.includes(themeName)) {
      console.warn(`BrandTheme: Unknown theme "${themeName}". Available: ${AVAILABLE_THEMES.join(', ')}`);
      return false;
    }

    const link = getStylesheetLink();
    const newHref = `${CDN_BASE}/${themeName}.css`;

    if (link.href !== newHref) {
      link.href = newHref;
    }

    currentTheme = themeName;

    if (options.persist) {
      try {
        localStorage.setItem(STORAGE_KEY_THEME, themeName);
      } catch (e) {
        // localStorage not available
      }
    }

    if (typeof options.onThemeChange === 'function') {
      options.onThemeChange(themeName);
    }

    return true;
  }

  /**
   * Set the color mode (light/dark/auto)
   */
  function setMode(mode) {
    if (!['light', 'dark', 'auto'].includes(mode)) {
      console.warn(`BrandTheme: Unknown mode "${mode}". Use 'light', 'dark', or 'auto'.`);
      return false;
    }

    const html = document.documentElement;

    if (mode === 'auto') {
      html.removeAttribute('data-theme');
      currentMode = 'auto';
    } else {
      html.setAttribute('data-theme', mode);
      currentMode = mode;
    }

    if (options.persist) {
      try {
        localStorage.setItem(STORAGE_KEY_MODE, mode);
      } catch (e) {
        // localStorage not available
      }
    }

    if (typeof options.onModeChange === 'function') {
      options.onModeChange(mode);
    }

    return true;
  }

  /**
   * Toggle between light and dark mode
   */
  function toggleMode() {
    const current = getEffectiveMode();
    setMode(current === 'dark' ? 'light' : 'dark');
  }

  /**
   * Get the effective mode (resolves 'auto' to actual value)
   */
  function getEffectiveMode() {
    if (currentMode === 'auto' || !currentMode) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return currentMode;
  }

  /**
   * Get stored preferences from localStorage
   */
  function getStoredPreferences() {
    try {
      return {
        theme: localStorage.getItem(STORAGE_KEY_THEME),
        mode: localStorage.getItem(STORAGE_KEY_MODE),
      };
    } catch (e) {
      return { theme: null, mode: null };
    }
  }

  /**
   * Initialize the theme switcher
   */
  function init(config) {
    // Handle string shorthand: BrandTheme.init('forest-night')
    if (typeof config === 'string') {
      config = { theme: config };
    }

    config = config || {};

    // Merge options
    if (config.persist !== undefined) options.persist = config.persist;
    if (config.onThemeChange) options.onThemeChange = config.onThemeChange;
    if (config.onModeChange) options.onModeChange = config.onModeChange;

    // Get stored preferences
    const stored = getStoredPreferences();

    // Determine theme (priority: config > stored > default)
    const theme = config.theme || stored.theme || 'forest-night';

    // Determine mode (priority: config > stored > 'auto')
    const mode = config.mode || stored.mode || 'auto';

    // Apply
    loadTheme(theme);
    setMode(mode);

    return BrandTheme;
  }

  /**
   * Public API
   */
  const BrandTheme = {
    init: init,
    theme: loadTheme,
    mode: setMode,
    toggle: toggleMode,
    getTheme: () => currentTheme,
    getMode: () => currentMode,
    getEffectiveMode: getEffectiveMode,
    themes: AVAILABLE_THEMES,
  };

  // Expose globally
  global.BrandTheme = BrandTheme;

})(typeof window !== 'undefined' ? window : this);
