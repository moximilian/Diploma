<template>
    <FormView displayName="groups" action="show" :defaults="entity"></FormView>
</template>
<script>
export default {
    data() {
        return {
            groupId: null,
            entity: null,
        }
    },
    created() {
        this.groupId = this.$route.params.id
        if (!this.groupId) {
            return console.error('User ID is not given')
        }
        this.$api.groups.one({ id: this.groupId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    },
}
</script>
