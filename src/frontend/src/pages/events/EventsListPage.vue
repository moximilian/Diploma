<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="events"
        :defaultFilters="defaultFilters"
        :filters="defaultFilters"
        clickRowPath="events"
    >
        <template #before="">
            <BaseBtn
                v-if="isGroupAdmin"
                @click="$router.push(`/events/new?group_id=${groupId}&name=${group.name}`)"
                >Добавить занятие</BaseBtn
            >
        </template>
    </TableView>
</template>
<script>
export default {
    props: {
        groupId: { type: String, default: () => '' },
        group: { type: Object, default: () => {} },
    },
    data() {
        return {
            keys: [
                { name: 'name', title: 'Название' },
                { name: 'description', title: 'Описание' },
                {
                    name: 'start_date',
                    title: 'Начало',
                    format: (_, value) => new Date(value).toShowDate(false),
                },
                { name: 'price', title: 'Цена', format: (_, value) => (value ?? 0) + ' .руб' },
            ],
        }
    },
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'group_id',
                            value: this.groupId,
                        },
                    ],
                },
            }
        },
        isGroupAdmin() {
            return this.group && (this.$ls.current_user == this.group?.creator_id ?? false)
        },
    },
}
</script>
