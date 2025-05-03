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
        async saveGroup(entity) {
            const { body, ok } = await this.$api.groups.insert({ ...entity })
            if (!ok) return
            this.$router.replace(`/groups/show/${body[0].id}`)
        },
    },
}
</script>
