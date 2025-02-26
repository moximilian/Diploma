<template>
    <TableView :keys="keys" displayName="groups" :defaultFilters="filters">
        <template #before>
            <BaseBtn @click="$router.replace('/groups/new')">Создать группу</BaseBtn>
        </template>
    </TableView>
</template>
<script>
export default {
    data() {
        return {
            keys: [
                { name: 'creator_id' },
                { name: 'name' },
                { name: 'description' },
                { name: 'is_open' },
                { name: 'max_participants_count' },
            ],
            userId: null,
        }
    },
    computed: {
        wheres() {
            return {
                column: this.userId === this.$ls.current_user ? 'creator_id' : 'participant_id',
                value: this.userId,
            }
        },
        filters() {
            return {
                filters: {
                    wheres: [this.wheres],
                },
            }
        },
    },
    created() {
        this.userId = this.$route.query?.user_id ?? this.$ls.current_user
    },
}
</script>
