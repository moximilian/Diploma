<template>
    <router-link to="/groups/list">My created groups</router-link>
    <FormBase displayName="groups" :defaults="entity"></FormBase>
</template>
<script>
export default {
    data() {
        return {
            userId: null,
            entity: null,
        }
    },
    created() {
        this.userId = this.$route.params.id
        if (!this.userId) {
            return console.error('User ID is not given')
        }
        this.$api.groups.one({ id: this.userId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
