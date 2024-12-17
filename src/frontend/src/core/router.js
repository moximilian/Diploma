import { createRouter, createWebHistory } from 'vue-router'

// import LoginPage from "@/pages/login/LoginPage.vue";

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
                routes.push({
                    path: `/${section.name}/${action}`, // Example: /persons/show
                    name: `${section.name}-${action}`, // Example: persons-show
                    component,
                })
            })
        }
    })

    return routes
}

// Helper function for capitalization
const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1)

// Define sections
const sections = [
    { name: 'home', actions: null },
    { name: 'auth', actions: ['login', 'register'] },
    { name: 'user', actions: ['show', 'edit'] },
]

// Generate routes
const routes = generateRoutes(sections)
console.log('RoutesBuild: ', routes)

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export { router }
