class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def starts_with(self, prefix: str, limit: int = 5):
        
        # prefix'e göre en fazla (limit) tane öneri döndürür.
        
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return []
            node = node.children[ch]

        results = []

        def dfs(cur_node, path_chars):
            if len(results) >= limit:
                return
            if cur_node.is_end:
                results.append(prefix + "".join(path_chars))
            for nxt in sorted(cur_node.children.keys()):
                dfs(cur_node.children[nxt], path_chars + [nxt])

        dfs(node, [])
        return results
