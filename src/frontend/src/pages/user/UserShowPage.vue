<template>
    <FormView displayName="user" :defaults="entity" action="show"></FormView>
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
        this.$api.users.one({ id: this.userId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
