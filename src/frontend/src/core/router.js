import { createRouter, createWebHistory } from 'vue-router'

function trimSlashes(value) {
    return value ? value.trim().replace(/^\/+|\/+$/g, '') : ''
}

function importComponent(component) {
    component = trimSlashes(component)
    return () =>
        component ? import(`@/pages/${component}.vue`) : import(`@/pages/Error404Page.vue`)
}

// Function to load components
const generateRoutes = sections => {
    const routes = []

    sections.forEach(section => {
        const defaultComponentName = `${capitalize(section.name)}Page`
        const defaultComponent = importComponent(`${section.name}/${defaultComponentName}`)

        if (!section?.actions?.length) {
            routes.push({
                path: `/${section.name}`, // Example: /login
                name: `${section.name}`, // Example: login
                component: defaultComponent,
            })
        } else {
            section.actions.forEach(action => {
                const component = importComponent(
                    `${section.name}/${capitalize(section.name)}${capitalize(action)}Page`
                )
                console.log(`${section.name}/${capitalize(section.name)}${capitalize(action)}Page`)
                let pathAction = `/:action(${action})`
                const path = section.useId ? `/${section.name}/${pathAction}/:id` : `/${section.name}/${pathAction}`
                routes.push({
                    path,
                    name: `${section.name}-${action}`,
                    component,
                })
            })
        }
    })

    return routes
}

// Helper function for capitalization
const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1)

// Define sections with useId property
const sections = [
    { name: 'home', actions: null, useId: false },
    { name: 'auth', actions: ['login', 'register'], useId: false },
    { name: 'user', actions: ['show', 'edit'], useId: true }, // useId is true for user actions
]

// Generate routes
const routes = generateRoutes(sections)
console.log('RoutesBuild: ', routes)

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export { router }
