local keymap = vim.keymap

local opts = { noremap = true, silent = true }

-- Directory Navigation
keymap.set("n", "<leader>m", ":NvimTreeFocus<CR>", opts)
keymap.set("n", "<leader>b", ":NvimTreeToggle<CR>", opts)

-- Pane Navigation
keymap.set("n", "<C-h>", "<C-w>h", opts) -- left
keymap.set("n", "<C-j>", "<C-w>j", opts) -- down
keymap.set("n", "<C-k>", "<C-w>k", opts) -- up
keymap.set("n", "<C-l>", "<C-w>l", opts) -- right

-- Window management
keymap.set("n", "<leader>sv", ":vsplit<CR>", opts) -- vertically
keymap.set("n", "<leader>sh", ":split<CR>", opts) -- horizontally
keymap.set("n", "<leader>sm", ":MaximizerToggle<CR>", opts) -- toggle minimize

-- Indenting
keymap.set("v", "<C-]>", ">gv", opts)
keymap.set("n", "<C-]>", "v>gvv", opts)
keymap.set("v", "<C-[>", "<gv", opts)
keymap.set("n", "<C-[>", "v<gvv", opts)

-- Comments
vim.api.nvim_set_keymap("n", "<C-_>", "gcc", { noremap = false })
vim.api.nvim_set_keymap("v", "<C-_>", "gcc", { noremap = false })
