import { createStore } from 'vuex'

export const store = createStore({
    currentUser() {
        return {
            id: null,
            photo64: null,
            photo_id: null
        }
    },
    getters: {
        currentUser(currentUser) {
            return currentUser
        }
    },


    mutations: {
        setUser(currentUser, id) {
            currentUser.id = id
        },
        setPhoto(currentUser, photo) {
            currentUser.photo64 = photo.image_data
            currentUser.photo_id = photo.id
        }
    },
})

console.info(store)
