<template>
    <NestedPage :title="entity?.name">
        <template #page-content>
            <FormView v-if="entity" displayName="groups" action="edit" :defaults="entity">
                <template #form-bottom="{ entity }">
                    <BaseBtn :outline="true" @click="toShow">Отменить</BaseBtn>
                    <BaseBtn @click="saveGroup(entity)">Сохранить</BaseBtn>
                </template>
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
    methods: {
        async saveGroup(entity) {
            const { ok } = await this.$api.groups.update({ ...entity, id: this.groupId })
            if (!ok) return
            this.$router.replace(`/groups/show/${this.groupId}`)
        },
        toShow() {
            this.$router.replace(`/groups/show/${this.groupId}`)
        },
    },
    async created() {
        this.groupId = this.$route.params.id
        if (!this.groupId) {
            return console.error('User ID is not given')
        }
        const { body, ok } = await this.$api.groups.one({ id: this.groupId })
        if (!ok) return console.error('Error during API call')
        this.entity = body
    },
}
</script>
