# UI Development Guide for Open WebUI

This guide provides comprehensive information about UI development standards, component libraries, and styling approaches used in Open WebUI. Following these guidelines ensures consistency across all applications and components.

> 💡 **Looking for code examples?** Check out [UI_DEVELOPMENT_EXAMPLES.md](UI_DEVELOPMENT_EXAMPLES.md) for practical component examples.

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Styling Approach](#styling-approach)
3. [Component Libraries](#component-libraries)
4. [Design System](#design-system)
5. [Best Practices](#best-practices)
6. [Common Patterns](#common-patterns)

## Technology Stack

Open WebUI's frontend is built with the following technologies:

### Core Framework
- **Svelte 5** - Modern reactive framework
- **SvelteKit** - Full-stack Svelte framework for building web applications
- **TypeScript** - Type-safe JavaScript

### Build Tools
- **Vite** - Fast build tool and development server
- **PostCSS** - CSS transformation pipeline

## Styling Approach

### Tailwind CSS v4

Open WebUI uses **Tailwind CSS v4** as the primary styling framework. This is the latest version of Tailwind with improved performance and new features.

**Why Tailwind CSS?**
- Utility-first approach enables rapid development
- Consistent design system through predefined utilities
- Dark mode support built-in
- Excellent tree-shaking for minimal production bundle size
- Type-safe with TypeScript integration

**Configuration:**
- Main config: `tailwind.config.js`
- Base styles: `src/tailwind.css`
- Global styles: `src/app.css`

#### Key Tailwind Plugins Used

1. **@tailwindcss/typography** - Beautiful typography defaults
2. **@tailwindcss/container-queries** - Container query support

#### Custom Theme Extensions

The project extends Tailwind's default theme with:

```javascript
// Custom gray scale colors with CSS variables
colors: {
  gray: {
    50: 'var(--color-gray-50, #f9f9f9)',
    100: 'var(--color-gray-100, #ececec)',
    // ... up to 950
  }
}
```

### When to Use Custom CSS

While Tailwind CSS is the primary styling method, custom CSS is acceptable in these cases:

1. **Complex animations** that are difficult to express with Tailwind utilities
2. **Global styles** that apply across the entire application (in `app.css`)
3. **Component-specific styles** that are highly reusable and complex
4. **Third-party integrations** that require specific CSS overrides

**Important:** Always prefer Tailwind utilities first. Only use custom CSS when Tailwind utilities are insufficient or would result in excessive repetition.

## Component Libraries

### Primary: bits-ui

**bits-ui** is the main component library used in Open WebUI. It provides headless, accessible components that you style with Tailwind CSS.

**What is bits-ui?**
- Headless component library for Svelte
- Provides unstyled, accessible components
- Full control over styling with Tailwind CSS
- ARIA compliant and keyboard accessible
- Based on Radix UI primitives

**Commonly Used bits-ui Components:**
- `DropdownMenu` - Context menus and dropdown menus
- `Switch` - Toggle switches
- `Dialog` - Modal dialogs
- `Popover` - Floating popovers
- `Tooltip` - Accessible tooltips

**Example Usage:**

```svelte
<script>
  import { DropdownMenu } from 'bits-ui';
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger>
    <button class="px-4 py-2 bg-blue-500 text-white rounded">
      Open Menu
    </button>
  </DropdownMenu.Trigger>
  <DropdownMenu.Content class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-2">
    <DropdownMenu.Item class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded">
      Item 1
    </DropdownMenu.Item>
  </DropdownMenu.Content>
</DropdownMenu.Root>
```

### Supporting Libraries

#### paneforge
Used for resizable split panes and layouts.

```svelte
import { PaneGroup, Pane, PaneResizer } from 'paneforge';
```

#### svelte-sonner
Toast notification system for user feedback.

```svelte
import { toast } from 'svelte-sonner';

toast.success('Operation completed!');
toast.error('Something went wrong');
```

### Why NOT Flowbite?

While Flowbite is a popular Tailwind component library, Open WebUI uses **bits-ui** instead for these reasons:

1. **Headless Architecture** - bits-ui gives full styling control without opinionated designs
2. **Svelte-First** - bits-ui is built specifically for Svelte, not adapted from React
3. **Accessibility** - Superior ARIA compliance and keyboard navigation
4. **Flexibility** - Easier to customize for Open WebUI's specific design needs
5. **Bundle Size** - Smaller footprint due to headless nature

## Design System

### Dark Mode

Open WebUI fully supports dark mode using Tailwind's `dark:` variant:

```svelte
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content adapts to theme
</div>
```

Dark mode is controlled by the `class` strategy in `tailwind.config.js`:

```javascript
darkMode: 'class'
```

### Color Palette

The custom gray scale uses CSS variables for runtime theming:

```css
--color-gray-50: #f9f9f9
--color-gray-100: #ececec
--color-gray-200: #e3e3e3
/* ... */
--color-gray-950: #0d0d0d
```

### Typography

Open WebUI uses a custom font stack:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Vazirmatn', 
  ui-sans-serif, system-ui, 'Segoe UI', Roboto, Ubuntu, Cantarell, 
  'Noto Sans', sans-serif;
```

Custom fonts loaded:
- **Inter** - Primary UI font (variable)
- **Archivo** - Alternative font (variable)
- **Mona Sans** - Display font
- **InstrumentSerif** - Secondary font for special elements
- **Vazirmatn** - RTL language support

### Responsive Design

Use Tailwind's responsive prefixes:

```svelte
<div class="w-full md:w-1/2 lg:w-1/3">
  Responsive width
</div>
```

### Spacing Scale

The application includes UI scaling support via CSS variables:

```css
:root {
  --app-text-scale: 1;
}
```

This allows users to scale the entire UI for accessibility.

## Best Practices

### 1. Component Organization

Organize components by feature:

```
src/lib/components/
├── common/          # Reusable UI components
├── admin/           # Admin-specific components
├── workspace/       # Workspace features
├── chat/            # Chat interface
├── icons/           # Icon components
└── layout/          # Layout components
```

### 2. Reusable Components

Create reusable components in `src/lib/components/common/`:

**Example: Custom Button Component**

```svelte
<!-- src/lib/components/common/Button.svelte -->
<script lang="ts">
  export let variant: 'primary' | 'secondary' | 'danger' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  
  const variantClasses = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600',
    danger: 'bg-red-600 hover:bg-red-700 text-white'
  };
  
  const sizeClasses = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg'
  };
</script>

<button 
  class="rounded transition {variantClasses[variant]} {sizeClasses[size]}"
  {...$$restProps}
>
  <slot />
</button>
```

### 3. Accessibility

Always consider accessibility:

- Use semantic HTML elements
- Include ARIA labels where appropriate
- Ensure keyboard navigation works
- Test with screen readers
- Maintain sufficient color contrast

Example:

```svelte
<button
  aria-label="Close dialog"
  aria-labelledby="dialog-title"
  type="button"
>
  <span id="dialog-title" class="sr-only">Close</span>
  <XIcon />
</button>
```

### 4. Type Safety

Use TypeScript for component props:

```svelte
<script lang="ts">
  export let id: string;
  export let disabled: boolean = false;
  export let onChange: (value: string) => void;
</script>
```

### 5. Internationalization

Use the i18n context for all user-facing text:

```svelte
<script lang="ts">
  import { getContext } from 'svelte';
  const i18n = getContext('i18n');
</script>

<button>{$i18n.t('Save Changes')}</button>
```

### 6. State Management

Use Svelte stores from `$lib/stores` for global state:

```svelte
<script>
  import { settings } from '$lib/stores';
</script>

{#if $settings?.darkMode}
  <div>Dark mode is enabled</div>
{/if}
```

## Common Patterns

### Modal Dialog Pattern

```svelte
<script>
  import Modal from '$lib/components/common/Modal.svelte';
  import { ConfirmDialog } from '$lib/components/common';
  
  let showModal = false;
</script>

<button onclick={() => showModal = true}>
  Open Modal
</button>

{#if showModal}
  <Modal bind:show={showModal} size="md">
    <div class="p-4">
      <h2 class="text-xl font-semibold mb-4">Modal Title</h2>
      <p>Modal content</p>
    </div>
  </Modal>
{/if}
```

### Dropdown Menu Pattern

```svelte
<script>
  import { DropdownMenu } from 'bits-ui';
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger>
    <button class="p-2">•••</button>
  </DropdownMenu.Trigger>
  
  <DropdownMenu.Content 
    class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-1"
  >
    <DropdownMenu.Item 
      class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer"
    >
      Edit
    </DropdownMenu.Item>
    <DropdownMenu.Item 
      class="px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer text-red-600"
    >
      Delete
    </DropdownMenu.Item>
  </DropdownMenu.Content>
</DropdownMenu.Root>
```

### Toast Notification Pattern

```svelte
<script>
  import { toast } from 'svelte-sonner';
  
  function handleAction() {
    try {
      // Perform action
      toast.success('Action completed successfully!');
    } catch (error) {
      toast.error('Action failed: ' + error.message);
    }
  }
</script>
```

### Form Input Pattern

```svelte
<script lang="ts">
  let value = '';
</script>

<div class="space-y-2">
  <label 
    for="input-id" 
    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
  >
    Field Label
  </label>
  <input
    id="input-id"
    type="text"
    bind:value
    placeholder="Enter value..."
    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 
           rounded-lg bg-white dark:bg-gray-800 
           focus:ring-2 focus:ring-blue-500 focus:outline-none"
  />
</div>
```

## Development Workflow

### 1. Running Development Server

```bash
npm run dev
```

Access the app at `http://localhost:5173`

### 2. Building for Production

```bash
npm run build
```

### 3. Type Checking

```bash
npm run check
```

### 4. Linting

```bash
npm run lint
```

### 5. Formatting

```bash
npm run format
```

## Testing Components

When creating new components:

1. Test in both light and dark modes
2. Test keyboard navigation
3. Test with different screen sizes (responsive)
4. Verify accessibility with tools like axe DevTools
5. Test with actual data, not just placeholders

## Resources

### Documentation
- [Svelte Documentation](https://svelte.dev/docs)
- [SvelteKit Documentation](https://kit.svelte.dev/docs)
- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
- [bits-ui Documentation](https://www.bits-ui.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

### Tools
- [Svelte DevTools](https://github.com/sveltejs/svelte-devtools)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [Svelte for VS Code](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode)

## Summary

**For Svelte Development in Open WebUI:**

| Question | Answer |
|----------|--------|
| **CSS Framework?** | **Tailwind CSS v4** (utility-first, with custom theme) |
| **Normal CSS?** | Only for complex cases where Tailwind is insufficient |
| **Component Library?** | **bits-ui** (headless, accessible components) |
| **Why not Flowbite?** | bits-ui offers better Svelte integration and flexibility |
| **Other UI Libraries?** | paneforge (layouts), svelte-sonner (toasts) |
| **Consistency?** | Follow this guide + use components from `src/lib/components/common/` |

**Key Principles:**
1. ✅ Use Tailwind CSS utilities for styling
2. ✅ Use bits-ui for interactive components (menus, switches, dialogs)
3. ✅ Create reusable components in `common/` directory
4. ✅ Support both light and dark modes
5. ✅ Ensure accessibility (ARIA, keyboard navigation)
6. ✅ Use TypeScript for type safety
7. ✅ Follow existing patterns in the codebase

By following these guidelines, all applications and components in Open WebUI will maintain a consistent look, feel, and behavior.
