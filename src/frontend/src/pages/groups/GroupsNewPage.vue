<template>
    <FormBase displayName="groups" @onSave="entity => saveUser(entity)">
    </FormBase>
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
            this.$api.groups.insert({ ...entity, id: this.userId }, res => {
                if (res.detail) return
                this.$router.replace(`/groups/show/${this.userId}`)
            })
        },
    },
    created() {
    },
}
</script>
