<template>
    <TableView
        ref="table"
        :keys="keys"
        displayName="participants"
        :defaultFilters="defaultFilters"
        :filters="defaultFilters"
        :isClickable="false"
    >
        <template #first-item="{ row }">
            <TableCellCheckBox @clickCheckBox="isChecked => onCheckboxChecked(isChecked, row)" />
        </template>
        <template #after-table>
            <BaseBtn value="Исключить" @click="removeParticipans" />
        </template>
    </TableView>
</template>

<script>
export default {
    props: {
        groupId: { type: String, default: () => '' },
    },
    data() {
        return {
            keys: [
                {
                    name: 'fio',
                    title: 'ФИО участника',
                    format: row => [row.name, row.surname, row.last_name].join(' '),
                },
                { name: 'login' },
            ],
            selectedIds: new Map(),
        }
    },
    methods: {
        onCheckboxChecked(isChecked, { id }) {
            isChecked ? this.selectedIds.set(id, true) : this.selectedIds.delete(id, true)
        },
        removeParticipans() {
            this.$api.participants.delete(
                { ids: Array.from(this.selectedIds).map(item => item[0]) },
                () => {
                    this.$refs.table.load()
                }
            )
        },
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
    },
}
</script>
