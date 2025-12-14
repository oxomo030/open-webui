# UI Development Guide - Example Components

This document provides practical examples of creating components following the Open WebUI standards.

## Example 1: Simple Button Component

This example demonstrates a reusable button component following Open WebUI's standards.

### File: `src/lib/components/common/Button.svelte`

```svelte
<script lang="ts">
	/**
	 * Reusable Button Component
	 * Follows Open WebUI styling standards with Tailwind CSS
	 */
	
	// Props with TypeScript types
	export let variant: 'primary' | 'secondary' | 'danger' | 'ghost' = 'primary';
	export let size: 'sm' | 'md' | 'lg' = 'md';
	export let disabled: boolean = false;
	export let type: 'button' | 'submit' | 'reset' = 'button';
	export let fullWidth: boolean = false;
	export let ariaLabel: string = '';
	
	// Variant classes for different button styles
	const variantClasses = {
		primary: 'bg-blue-600 hover:bg-blue-700 text-white disabled:bg-blue-400',
		secondary: 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-white',
		danger: 'bg-red-600 hover:bg-red-700 text-white disabled:bg-red-400',
		ghost: 'bg-transparent hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
	};
	
	// Size classes
	const sizeClasses = {
		sm: 'px-2 py-1 text-sm',
		md: 'px-4 py-2',
		lg: 'px-6 py-3 text-lg'
	};
</script>

<button
	{type}
	{disabled}
	aria-label={ariaLabel}
	class="rounded-lg font-medium transition-colors duration-200
		focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
		disabled:cursor-not-allowed disabled:opacity-50
		{variantClasses[variant]}
		{sizeClasses[size]}
		{fullWidth ? 'w-full' : ''}"
	{...$$restProps}
	on:click
>
	<slot />
</button>

<!-- Usage Examples:

1. Primary Button (default):
<Button on:click={handleClick}>
	Click Me
</Button>

2. Secondary Button with icon:
<Button variant="secondary" size="sm">
	<PlusIcon class="w-4 h-4 mr-2" />
	Add Item
</Button>

3. Danger Button (full width):
<Button variant="danger" fullWidth={true}>
	Delete Account
</Button>

4. Disabled Button:
<Button disabled={true}>
	Processing...
</Button>

-->
```

## Example 2: Form Input with Label

This example shows a form input component with proper accessibility and theming.

### File: `src/lib/components/common/FormInput.svelte`

```svelte
<script lang="ts">
	import { getContext } from 'svelte';
	
	// i18n context for internationalization
	const i18n = getContext('i18n');
	
	// Props
	export let id: string;
	export let label: string;
	export let value: string = '';
	export let type: 'text' | 'email' | 'password' | 'number' | 'url' = 'text';
	export let placeholder: string = '';
	export let required: boolean = false;
	export let disabled: boolean = false;
	export let error: string = '';
	export let helpText: string = '';
	
	// Generate unique IDs for accessibility
	const helpTextId = `${id}-help`;
	const errorId = `${id}-error`;
</script>

<div class="space-y-2">
	<!-- Label -->
	<label
		for={id}
		class="block text-sm font-medium text-gray-700 dark:text-gray-300"
	>
		{label}
		{#if required}
			<span class="text-red-500" aria-label={$i18n.t('Required')}>*</span>
		{/if}
	</label>
	
	<!-- Input Field -->
	<input
		{id}
		{type}
		{placeholder}
		{required}
		{disabled}
		bind:value
		aria-describedby={helpText ? helpTextId : error ? errorId : undefined}
		aria-invalid={error ? 'true' : 'false'}
		class="w-full px-3 py-2 border rounded-lg
			bg-white dark:bg-gray-800
			text-gray-900 dark:text-white
			placeholder:text-gray-400 dark:placeholder:text-gray-500
			transition-colors duration-200
			focus:outline-none focus:ring-2 focus:ring-blue-500
			disabled:opacity-50 disabled:cursor-not-allowed
			{error
				? 'border-red-500 focus:ring-red-500'
				: 'border-gray-300 dark:border-gray-600'}"
		{...$$restProps}
		on:input
		on:change
		on:blur
		on:focus
	/>
	
	<!-- Help Text -->
	{#if helpText && !error}
		<p id={helpTextId} class="text-sm text-gray-500 dark:text-gray-400">
			{helpText}
		</p>
	{/if}
	
	<!-- Error Message -->
	{#if error}
		<p id={errorId} class="text-sm text-red-600 dark:text-red-400" role="alert">
			{error}
		</p>
	{/if}
</div>

<!-- Usage Example:

<script>
	let email = '';
	let emailError = '';
	
	function validateEmail() {
		if (!email.includes('@')) {
			emailError = 'Please enter a valid email address';
		} else {
			emailError = '';
		}
	}
</script>

<FormInput
	id="user-email"
	label="Email Address"
	type="email"
	placeholder="you@example.com"
	required={true}
	helpText="We'll never share your email with anyone else."
	bind:value={email}
	error={emailError}
	on:blur={validateEmail}
/>

-->
```

## Example 3: Card Component with Dark Mode

This example demonstrates a card component with proper dark mode support.

### File: `src/lib/components/common/Card.svelte`

```svelte
<script lang="ts">
	/**
	 * Card Component
	 * Provides a container with consistent styling
	 */
	
	export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
	export let shadow: boolean = true;
	export let hover: boolean = false;
	export let className: string = '';
	
	const paddingClasses = {
		none: 'p-0',
		sm: 'p-3',
		md: 'p-4',
		lg: 'p-6'
	};
</script>

<div
	class="rounded-lg border
		bg-white dark:bg-gray-900
		border-gray-200 dark:border-gray-800
		{shadow ? 'shadow-md' : ''}
		{hover ? 'transition-shadow hover:shadow-lg' : ''}
		{paddingClasses[padding]}
		{className}"
	{...$$restProps}
>
	<slot />
</div>

<!-- Usage Example:

<Card padding="lg" shadow={true} hover={true}>
	<h3 class="text-xl font-semibold mb-2">Card Title</h3>
	<p class="text-gray-600 dark:text-gray-400">
		This is the card content with proper dark mode support.
	</p>
</Card>

-->
```

## Example 4: Dropdown Menu with bits-ui

This example shows how to use bits-ui for accessible dropdown menus.

### File: `src/lib/components/common/ActionsMenu.svelte`

```svelte
<script lang="ts">
	import { DropdownMenu } from 'bits-ui';
	import { getContext } from 'svelte';
	
	// Icons (assuming these exist in your project)
	import EllipsisHorizontal from '$lib/components/icons/EllipsisHorizontal.svelte';
	import PencilSquare from '$lib/components/icons/PencilSquare.svelte';
	import TrashIcon from '$lib/components/icons/Trash.svelte';
	
	const i18n = getContext('i18n');
	
	// Events that can be dispatched
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
</script>

<DropdownMenu.Root>
	<DropdownMenu.Trigger asChild let:builder>
		<button
			use:builder.action
			{...builder}
			class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 
				transition-colors duration-200"
			aria-label={$i18n.t('Actions')}
		>
			<EllipsisHorizontal className="w-5 h-5" />
		</button>
	</DropdownMenu.Trigger>
	
	<DropdownMenu.Content
		class="min-w-[12rem] bg-white dark:bg-gray-800 
			border border-gray-200 dark:border-gray-700
			rounded-lg shadow-lg p-1 z-50"
		sideOffset={5}
	>
		<!-- Edit Action -->
		<DropdownMenu.Item
			class="flex items-center gap-2 px-3 py-2 text-sm
				hover:bg-gray-100 dark:hover:bg-gray-700
				rounded cursor-pointer
				text-gray-700 dark:text-gray-300
				transition-colors duration-200"
			on:click={() => dispatch('edit')}
		>
			<PencilSquare className="w-4 h-4" />
			<span>{$i18n.t('Edit')}</span>
		</DropdownMenu.Item>
		
		<!-- Separator -->
		<DropdownMenu.Separator class="h-px bg-gray-200 dark:bg-gray-700 my-1" />
		
		<!-- Delete Action (danger style) -->
		<DropdownMenu.Item
			class="flex items-center gap-2 px-3 py-2 text-sm
				hover:bg-red-50 dark:hover:bg-red-900/20
				rounded cursor-pointer
				text-red-600 dark:text-red-400
				transition-colors duration-200"
			on:click={() => dispatch('delete')}
		>
			<TrashIcon className="w-4 h-4" />
			<span>{$i18n.t('Delete')}</span>
		</DropdownMenu.Item>
	</DropdownMenu.Content>
</DropdownMenu.Root>

<!-- Usage Example:

<script>
	function handleEdit() {
		console.log('Edit clicked');
	}
	
	function handleDelete() {
		console.log('Delete clicked');
	}
</script>

<ActionsMenu
	on:edit={handleEdit}
	on:delete={handleDelete}
/>

-->
```

## Example 5: Toast Notifications

This example demonstrates using svelte-sonner for notifications.

### Usage in any component:

```svelte
<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { getContext } from 'svelte';
	
	const i18n = getContext('i18n');
	
	async function saveData() {
		try {
			// Perform save operation
			await api.save(data);
			
			// Success notification
			toast.success($i18n.t('Data saved successfully!'));
		} catch (error) {
			// Error notification
			toast.error($i18n.t('Failed to save data: ') + error.message);
		}
	}
	
	function showInfo() {
		toast.info($i18n.t('Processing your request...'));
	}
	
	function showWarning() {
		toast.warning($i18n.t('This action cannot be undone'));
	}
	
	function showCustomToast() {
		toast.custom({
			component: CustomToastComponent,
			componentProps: {
				title: 'Custom Toast',
				message: 'With custom styling'
			}
		});
	}
</script>
```

## Best Practices Demonstrated

All examples above demonstrate:

1. **TypeScript Usage** - Props are typed for safety
2. **Tailwind CSS** - All styling uses Tailwind utilities
3. **Dark Mode Support** - `dark:` variants for theming
4. **Accessibility** - ARIA labels, semantic HTML, keyboard navigation
5. **Internationalization** - Using i18n context for text
6. **Event Forwarding** - Using `on:click` and `dispatch` for events
7. **Reusability** - Components accept props and slots
8. **Consistent Naming** - Clear, descriptive prop and variable names
9. **Focus States** - Visible focus rings for keyboard users
10. **Transitions** - Smooth animations with Tailwind transitions

## Testing Your Components

When creating components, test them in:

1. **Light and Dark Mode** - Toggle theme to verify
2. **Different Screen Sizes** - Use responsive design tools
3. **With Keyboard** - Navigate without mouse
4. **With Screen Reader** - Test accessibility
5. **Different States** - Disabled, error, loading, etc.

## Additional Resources

- See `src/lib/components/common/` for more examples
- Review the [UI Development Guide](UI_DEVELOPMENT.md) for complete standards
- Check existing components before creating new ones
