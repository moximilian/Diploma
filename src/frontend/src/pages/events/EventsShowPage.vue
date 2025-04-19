<template>
    <NestedPage title="Просмотр занятия">
        <template #page-content>
            <FormView action="show" displayName="events" >
            </FormView>
        </template>
    </NestedPage>
</template>
<script>
export default {
    data() {
        return {
            eventId: null,
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
    created() {
        this.eventId = this.$route.params.id
        if (!this.eventId) {
            return console.error('Event ID is not given')
        }
        this.$api.events.one({ id: this.eventId }, res => {
            if (res.detail) return console.error('Error during API call')
            this.entity = res
        })
    }
}
</script>
