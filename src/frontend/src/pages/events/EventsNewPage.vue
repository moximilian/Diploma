<template>
    <NestedPage
        :title="`Создать занятие ${groupName && 'для группы ' + groupName}`"
        v-if="!isStudent"
    >
        <template #page-content>
            <FormView
                action="new"
                displayName="events"
                :defaults="{ group_id: groupId }"
                @onSave="async entity => await saveEvent(entity)"
            >
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
        },
    },
    methods: {
        async saveEvent(entity) {
            const { body, ok } = await this.$api.events.insert({
                ...entity,
                group_id: this.$route.query.group_id,
            })
            if (!ok) return
            this.$router.replace(`/events/show/${body[0].id}`)
        },
    },
}
</script>
