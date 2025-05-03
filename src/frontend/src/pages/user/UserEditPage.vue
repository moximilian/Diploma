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
            <div
                v-if="!isStudent"
                :class="{ selected: isSelected('slots') }"
                @click="select('slots')"
            >
                Мои слоты
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
                <div class="page-content" v-if="isSelected('security')">
                    <FormView displayName="passwordChange" action="edit">
                        <template #form-bottom="{ entity }">
                            <BaseBtn @click="updatePassword(entity)">Изменить пароль</BaseBtn>
                        </template>
                    </FormView>
                </div>
                <div class="page-content" v-if="isSelected('slots')">
                    <SlotsListPage :userId="userId" />
                </div>
            </div>
        </template>
    </NestedPage>
</template>
<script>
import SlotsListPage from '@/pages/slots/SlotsListPage.vue'
import TabsMixin from '@/pages/_help/TabsMixin'
export default {
    mixins: [TabsMixin],
    components: { SlotsListPage },
    data() {
        return {
            userId: null,
            entity: null,

            selectedOption: 'personalInfo',
        }
    },
    methods: {
        async saveUser(entity) {
            const { ok } = await this.$api.users.update({
                ...entity,
                id: this.userId,
                is_external_auth: this.entity.is_external_auth,
            })
            if (!ok) return
            await this.fetchUser()
        },
        async updatePassword(entity) {
            await this.$api.users.change_password({ ...entity })
        },
        async fetchUser() {
            const { body, ok } = await this.$api.users.one({ id: this.userId })
            if (!ok) return console.error('Error during API call')
            this.entity = body
            if (body?.photo_id && !this.imageSrc) await this.fetchImage(body.photo_id)
        },
        async fetchImage(id) {
            const { body } = await this.$api.images.get({ id })
            this.$store.commit('setPhoto', body)
        },
        async uploadImage(image_data, image_name) {
            const { ok } = await this.$api.images.set_user({
                image_name,
                image_data,
            })
            if (!ok) return
            await this.fetchUser()
        },
        async deleteImage() {
            const { ok } = await this.$api.images.delete_user({
                id: this.$store.state.photo_id,
            })
            if (!ok) return
            this.$store.commit('setPhoto', { image_data: null, id: null })
        },
    },
    computed: {
        imageSrc() {
            return this.$store.state.photo64
        },
        isStudent() {
            return this.$store.getters.isStudent
        },
    },
    async created() {
        this.userId = this.$route.params.id
        if (!this.userId) {
            return console.error('User ID is not given')
        }
        await this.fetchUser()
    },
}
</script>
