<template>
    <FormView  action="new" displayName="groups" @onSave="entity => saveGroup(entity)">
    </FormView>
</template>
<script>
export default {
    data() {
        return {
            groupId: null,
            entity: null,
        }
    },
    methods: {
        saveGroup(entity) {
            this.$api.groups.insert({ ...entity}, res => {
                if (res.detail) return
                this.$router.replace(`/groups/show/${this.groupId}`)
            })
        },
    },
    created() {
    },
}
</script>
