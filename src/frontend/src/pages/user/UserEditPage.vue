<template>
    <FormView
        displayName="user"
        action="edit"
        :defaults="entity"
    >
    <template #form-bottom="{entity}">
        <BaseBtn @click="saveUser(entity)">Сохранить</BaseBtn>
        <BaseBtn @click="toShow">Назад</BaseBtn>
    </template>
    </FormView>
</template>
<script>
export default {
    data() {
        return {
            userId: null,
            entity: null,
        }
    },
    methods: {
        saveUser(entity) {
            this.$api.users.update({ ...entity, id: this.userId }, res => {
                if (res.detail) return
                this.$router.replace(`/user/show/${this.userId}`)
            })
        },
        toShow() {
            this.$router.replace(`/user/show/${this.userId}`)
        }
    },
    created() {
        this.userId = this.$route.params.id
        if (!this.userId) {
            return console.error('User ID is not given')
        }
        this.$api.users.one({ id: this.userId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
