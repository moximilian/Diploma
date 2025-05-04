export default {
    data() {
        return {
            keys: [{ name: 'user_id' }],
            checkBoxKeys: [{ name: 'is_attended' }, { name: 'is_paid' }],
            slotId: '',

            newCustomKey: '',
            isShowCustomInput: false,
            customKeysForTable: [],
        }
    },
    methods: {
        setValueForCustomField: async function (name, value, row) {
            row.custom[name] = value
            await this.updateRow(row)
        }.debounce(1000),
        setNewCustomTitle(newTitle) {
            this.newCustomKey = newTitle
        },
        deleteCustomKey(key, rows) {
            if (!Array.isArray(rows)) return
            rows.forEach(async row => {
                if (row?.custom && key in row.custom) {
                    delete row.custom[key]
                    await this.updateRow(row)
                }
            })
        },
        addNewCustomTitle(rows) {
            this.toggleCustomInput()

            rows.forEach(async row => {
                row = this.transformEntity(row)
                row.custom[this.newCustomKey] = null
                await this.updateRow(row)
            })
            this.newCustomKey = ''
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
        async onCheckedChange(isChecked, name, entity) {
            entity = this.transformEntity(entity)
            entity[name] = isChecked
            await this.updateRow(entity)
        },
    },
}
