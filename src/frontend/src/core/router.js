import { createRouter, createWebHistory } from 'vue-router'
import { store } from './store'
import LocalStorage from '@/core/LocalStorage'
console.log(store.state, 'info')
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
                path: `/${section.name}`,
                name: `${section.name}`,
                component: defaultComponent,
            })
        } else {
            section.actions.forEach(action => {
                const component = importComponent(
                    `${section.name}/${capitalize(section.name)}${capitalize(action)}Page`
                )
                console.log(`${section.name}/${capitalize(section.name)}${capitalize(action)}Page`)
                let pathAction = `/:action(${action})`
                const path =
                    section.useId && !['list', 'new'].includes(action)
                        ? `/${section.name}/${pathAction}/:id`
                        : `/${section.name}/${pathAction}`
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
    { name: 'auth', actions: ['login', 'register'], useId: false },
    { name: 'home', actions: null, useId: false },
    { name: 'user', actions: ['show', 'edit'], useId: true },
    { name: 'groups', actions: ['list', 'show', 'edit', 'new'], useId: true },
]

// Generate routes
const routes = generateRoutes(sections)

routes.push(
    {
        path: '/auth/yandex-callback',
        component: () => import('@/pages/auth/YandexCallback.vue'),
    },
    {
        path: '/:catchAll(.*)',
        redirect: () => {
            return { path: '/home', query: {} }
        },
    }
)
console.log('RoutesBuild: ', routes)

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach(to => {
    console.log(to, store.getters.isUserSet)
    if (
        !to.path.includes('auth') &&
        [null, undefined, ''].includes(new LocalStorage().getItemDecrypt('token'))
    ) {
        return { path: '/auth/login' }
    }
})

export { router }
