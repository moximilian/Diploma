<template>
    <div>
        <TableView
            ref="table"
            :keys="[...keys, ...checkBoxKeys, ...customKeysForTable]"
            displayName="eventParticipant"
            :defaultFilters="defaultFilters"
            :filters="defaultFilters"
            orderByLocal="datetime"
            :isClickable="false"
            @loaded="getCustomKeysForTable"
            @onCustomKeyDelete="deleteCustomKey"
        >
            <template #before>
                <BaseBtn @click="addAllParticipants">Добавить всех участников группы</BaseBtn>
            </template>
            <template #table-cell="{ row, keyObj }">
                <TableCellCheckBox
                    v-if="checkBoxKeys.includes(keyObj)"
                    :isCheckedDefault="row[keyObj.name]"
                    @clickCheckBox="isChecked => onCheckedChange(isChecked, keyObj.name, row)"
                />
                <div v-if="keyObj?.isCustom === true">
                    <InputField
                        :value="row.custom?.[keyObj.name]"
                        :ref="`input${keyObj.name}${row.id}`"
                        @changeValue="value => setValueForCustomField(keyObj.name, value, row)"
                    />
                </div>
            </template>
            <template #custom-title-key="{ rows }">
                <div class="table-cell">
                    <div class="flex-container-column">
                        <div class="flex-container-row" v-if="!isShowCustomInput">
                            Добавить новую характеристику
                            <BaseBtn class="small" :outline="true" @click="toggleCustomInput"
                                >+</BaseBtn
                            >
                        </div>
                        <div class="flex-container-row" v-if="isShowCustomInput">
                            <InputField placeholder="Например, ДЗ" @changeValue="setNewCustomTitle" />
                            <BaseBtn
                                class="small"
                                :outline="true"
                                :disabled="!newCustomKey"
                                @click="() => addNewCustomTitle(rows)"
                                >+</BaseBtn
                            >
                        </div>
                    </div>
                </div>
            </template>
            <template #last-item="{ row }">
                <TableCell>
                    <BaseBtn @click="deleteEventParticipant(row.id)">Удалить участника</BaseBtn>
                </TableCell>
            </template>
        </TableView>
    </div>
</template>
<script>
export default {
    data() {
        return {
            keys: [{ name: 'user_id' }],
            checkBoxKeys: [{ name: 'is_attended' }, { name: 'is_paid' }],
            eventId: '',

            newCustomKey: '',
            isShowCustomInput: false,
            customKeysForTable: [],
        }
    },
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'event_id',
                            value: this.eventId,
                        },
                    ],
                },
            }
        },
    },
    methods: {
        setValueForCustomField: function (name, value, row) {
            row.custom[name] = value
            this.updateRow(row)
        }.debounce(1000),
        setNewCustomTitle(newTitle) {
            this.newCustomKey = newTitle
        },
        deleteCustomKey(key, rows) {
            if (!Array.isArray(rows)) return
            rows.forEach(row => {
                if (row?.custom && key in row.custom) {
                    delete row.custom[key]
                    this.updateRow(row)
                }
            })
        },
        addNewCustomTitle(rows) {
            this.toggleCustomInput()

            rows.forEach(row => {
                row = this.transformEntity(row)
                row.custom[this.newCustomKey] = null
                this.updateRow(row)
            })
        },
        toggleCustomInput() {
            this.isShowCustomInput = !this.isShowCustomInput
        },
        getCustomKeysForTable(rows) {
            const custom = rows.at(0)?.custom ?? {}
            this.customKeysForTable = Object.keys(custom).reduce((keys, customKey) => {
                keys.push({ title: customKey, name: customKey, isCustom: true })
                return keys
            }, [])
        },
        addAllParticipants() {
            this.$api.eventParticipant.add_all({ id: this.eventId }, () => {
                this.$refs.table.load()
            })
        },
        transformEntity(entity) {
            return Object.entries(entity).reduce((entity, [key, value]) => {
                if (value === null) {
                    if (this.checkBoxKeys.map(item => item.name).includes(key)) value = false
                    else value = {}
                }
                entity[key] = value
                return entity
            }, entity)
        },
        updateRow(entity, cb) {
            this.$api.eventParticipant.update(entity, () => {
                this.$refs.table.load()
                cb?.()
            })
        },
        onCheckedChange(isChecked, name, entity) {
            entity = this.transformEntity(entity)
            entity[name] = isChecked
            this.updateRow(entity)
        },
        deleteEventParticipant(id) {
            this.$api.eventParticipant.delete({ id }, () => {
                this.$refs.table.load()
            })
        },
    },
    created() {
        this.eventId = this.$route.params.id
    },
}
</script>
