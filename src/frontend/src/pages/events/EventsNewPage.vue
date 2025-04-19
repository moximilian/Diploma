<template>
    <NestedPage :title="`Создать занятие ${groupName && 'для группы ' + groupName}`" v-if="!isStudent">
        <template #page-content>
            <FormView action="new" displayName="events" @onSave="entity => saveEvent(entity)">
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
        groupName() {
            return this.$route.query.name ?? ''
        }
    },
    methods: {
        saveEvent(entity) {
            this.$api.events.insert({ ...entity, group_id: this.$route.query.group_id }, res => {
                if (res.detail) return
                this.$router.replace(`/events/show/${res[0].id}`)
            })
        },
    },
}
</script>
