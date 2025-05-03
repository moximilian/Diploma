<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="slots"
        :defaultFilters="defaultFilters"
        :filters="defaultFilters"
        clickRowPath="slots"
    >
        <!-- <template #before="">
            <BaseBtn
                v-if="isGroupAdmin"
                @click="$router.push(`/events/new?group_id=${userId}&name=${group.name}`)"
                >Добавить занятие</BaseBtn
            >
        </template> -->
    </TableView>
</template>
<script>
export default {
    props: {
        userId: { type: String, default: () => '' },
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
                {
                    name: 'time',
                    title: 'Время',
                    format: row => `${row.start_time} - ${row.end_time}`,
                },
                {
                    name: 'max_participants_count',
                    title: 'Количество участнков',
                    format: row => `${row.participants_count}/${row.max_participants_count}`,
                },
            ],
        }
    },
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'creator_id',
                            value: this.userId,
                        },
                    ],
                },
            }
        },
    },
}
</script>
