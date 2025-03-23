import { createStore } from 'vuex'

export const store = createStore({
    state() {
        return {
            id: null,
            photo64: null,
            photo_id: null,
            roleName: null,
        }
    },

    getters: {
        isStudent(state) {
            return state.roleName === 'student'
        },
        isTeacher(state) {
            return state.roleName === 'teacher'
        },
    },

    mutations: {
        setUser(state, id) {
            state.id = id
        },
        setPhoto(state, photo) {
            state.photo64 = photo.image_data
            state.photo_id = photo.id
        },
        setRole(state, roleName) {
            state.roleName = roleName
        },
    },
})

console.info(store.state, 'store')
