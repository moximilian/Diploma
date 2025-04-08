<template>
    <NestedPage title="Профиль">
        <template #page-header-right>
            <div :class="{ selected: isSelected('personalInfo') }" @click="select('personalInfo')">
                Персональная информация
            </div>
            <div
                v-if="!entity?.is_external_auth"
                :class="{ selected: isSelected('security') }"
                @click="select('security')"
            >
                Безопасность
            </div>
        </template>

        <template #page-content>
            <div>
                <div class="page-content" v-if="isSelected('personalInfo')">
                    <FormView v-if="entity" displayName="user" action="edit" :defaults="entity">
                        <template #form-bottom="{ entity }">
                            <BaseBtn @click="saveUser(entity)">Сохранить</BaseBtn>
                        </template>
                    </FormView>
                    <div class="image-container">
                        <PhotoField :src="imageSrc" />
                        <div class="image-controls">
                            <UploadBtn
                                :outline="true"
                                text="Загрузить"
                                accept=".jpg, .png, .jpeg"
                                @onclick="uploadImage"
                            />
                            <BaseBtn :outline="true" :disabled="!imageSrc" @click="deleteImage"
                                >Удалить</BaseBtn
                            >
                        </div>
                    </div>
                </div>
                <div class="page-content" v-else>
                    <FormView displayName="passwordChange" action="edit">
                        <template #form-bottom="{ entity }">
                            <BaseBtn @click="updatePassword(entity)">Изменить пароль</BaseBtn>
                        </template>
                    </FormView>
                </div>
            </div>
        </template>
    </NestedPage>
</template>
<script>
import TabsMixin from '@/pages/_help/TabsMixin'
export default {
    mixins: [TabsMixin],
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
            this.$api.users.change_password({ ...entity }, res => {
                if (res.detail) return
            })
        },
        fetchUser() {
            this.$api.users.one({ id: this.userId }, res => {
                if (res.detail) return console.error('Error during API call')
                this.entity = res
                if (res?.photo_id && !this.imageSrc) this.fetchImage(res.photo_id)
            })
        },
        fetchImage(id) {
            this.$api.images.get({ id }, res => {
                this.$store.commit('setPhoto', res)
            })
        },
        uploadImage(image_data, image_name) {
            this.$api.images.set_user(
                {
                    image_name,
                    image_data,
                },
                res => {
                    if (res?.detail) return
                    this.fetchUser()
                }
            )
        },
        deleteImage() {
            this.$api.images.delete_user({ id: this.$store.state.photo_id }, res => {
                if (res?.detail) return
                this.$store.commit('setPhoto', { image_data: null, id: null })
            })
        },
    },
    computed: {
        imageSrc() {
            return this.$store.state.photo64
        },
    },
    created() {
        this.userId = this.$route.params.id
        if (!this.userId) {
            return console.error('User ID is not given')
        }
        this.fetchUser()
    },
}
</script>
