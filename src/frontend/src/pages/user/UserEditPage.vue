<template>
    <div class="page-user-container">
        <div class="page user">
            <div class="select-toggle-wrapper">
                <div class="page-title">
                    Профиль
                </div>

                <div class="select-toggle">
                    <div :class="{selected: isUserEditSelected}" @click="select('personalInfo')">Персональная информация</div>
                    <div :class="{selected: !isUserEditSelected}" @click="select('security')">Безопасность</div>
                </div>
            </div>

            <div>
                <div class="user-form-container" v-if="isUserEditSelected">
                    <FormView displayName="user" action="edit" :defaults="entity">
                        <template #form-bottom="{ entity }">
                            <BaseBtn @click="saveUser(entity)">Сохранить</BaseBtn>
                            
                        </template>
                    </FormView>
                    <div class="image-container">
                        <PhotoField :src="imageSrc"/>
                        <div class="image-controls">
                            <UploadBtn :outline="true" text="Загрузить" accept=".jpg, .png, .jpeg" @onclick="uploadImage"/>
                            <BaseBtn :outline="true" :disabled="!imageSrc" @click="deleteImage">Удалить</BaseBtn>
                        </div>
                    </div>
                </div>
                <div class="user-form-container" v-else>
                    <FormView displayName="passwordChange" action="edit">
                        <template #form-bottom="{ entity }">
                            <BaseBtn @click="updatePassword(entity)">Изменить пароль</BaseBtn>
                        </template>
                    </FormView>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.page-user-container {
    display: flex;
    width: 100%;
    justify-content: center;
}

.page.user {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 1280px;
}

.select-toggle-wrapper {
    display: flex;
    flex-direction: row;
    align-content: center;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid var(--gray-color);

}
.select-toggle {
    display: flex;
    flex-direction: row;
    gap: 80px;

    height: 100%;
    align-items: center;
}
.select-toggle div.selected {
    display:flex;
    height: 100%;

    align-items: center;
    color: var(--main-color);
    border-bottom: 2px solid var(--gray-color);
    border-color: var(--main-color);
}

.user-form-container {
    display: flex;
    flex-direction: row;
    gap: 120px;
}

.image-container {
    margin-top: 32px;

    display: flex;
    flex-direction: row;
    gap: 16px;
}
.image-container img {
    width: 112px;
    height:112px;

    border-radius: 8px;
}
.image-controls {
    display: flex;
    flex-direction: column;
    gap:16px;
}


</style>
<script>
export default {
    data() {
        return {
            userId: null,
            entity: null,

            selectedOption: 'personalInfo',
        }
    },
    methods: {
        saveUser(entity) {
            this.$api.users.update({ ...entity, id: this.userId }, res => {
                if (res.detail) return
                this.fetchUser()
            })
        },
        updatePassword(entity) {
            this.$api.users.change_password({...entity}, (res) => {
                if (res.detail) return

            })
        },

        select(option) {
            this.$router.push(`/user/edit/${this.userId}?tab=${option}`)
        },
        fetchUser() {
            this.$api.users.one({ id: this.userId }, res => {
                if (res.detail) return console.error('Error during API call')
                this.entity = res
                if (res?.photo_id && !this.imageSrc) this.fetchImage(res.photo_id)
            })
        },
        fetchImage(id) {
            this.$api.images.get({id}, (res) => {
                this.$store.commit('setPhoto', res)
            })
        },
        uploadImage(image_data, image_name) {
            this.$api.images.set_user({
                image_name, image_data
            }, (res) => {
                if (res?.detail) return
                this.fetchUser()
            })
        },
        deleteImage() {
            this.$api.images.delete_user({id: this.$store.state.photo_id}, (res) => {
                if (res?.detail) return
                this.$store.commit('setPhoto', {image_data: null, id: null})
            })
        }
    },
    computed: {
        isUserEditSelected() {
            return this.selectedOption === 'personalInfo'
        },
        imageSrc() {
            return this.$store.state.photo64
        },
        queryTab() {
            return this.$route.query?.tab ?? 'personalInfo'
        }
    },
    watch: {
        queryTab() {
            this.selectedOption = this.queryTab 
        }
    },
    created() {
        this.selectedOption = this.queryTab 
        this.userId = this.$route.params.id
        if (!this.userId) {
            return console.error('User ID is not given')
        }
        this.fetchUser()

    },
}
</script>
