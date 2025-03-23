<template>
    <NestedPage title="Создать группу" v-if="!isStudent">
        <template #page-content>
            <FormView action="new" displayName="groups" @onSave="entity => saveGroup(entity)">
            </FormView>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            groupId: null,
            entity: null,
        }
    },
    computed: {
        isStudent() {
            return this.$store.getters.isStudent
        },
    },
    methods: {
        saveGroup(entity) {
            this.$api.groups.insert({ ...entity }, res => {
                if (res.detail) return
                this.$router.replace(`/groups/show/${res[0].id}`)
            })
        },
    },
}
</script>
