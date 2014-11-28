
public class BalancedTree {
    static class BinaryTreeNode {
        int value;
        BinaryTreeNode left;
        BinaryTreeNode right;

        BinaryTreeNode(int value, BinaryTreeNode left, BinaryTreeNode right) {
            this.value = value;
            this.left = left;
            this.right = right;
        }
    }

    boolean isBalanced(BinaryTreeNode root, int max, int min) {
        if (root == null) return true;

        if (root.value > max || root.value < min)
            return false;
        else return isBalanced(root.left, root.value, min) && isBalanced(root.right, max, root.value);

    }


    public static void main(String args[]) {

        BalancedTree bt = new BalancedTree();

        //one node
        {
            BinaryTreeNode oneNode = new BinaryTreeNode(100, null, null);

            System.out.println(bt.isBalanced(oneNode, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }

        //two level--balanced
        {
            BinaryTreeNode node2left = new BinaryTreeNode(50, null, null);
            BinaryTreeNode node2right = new BinaryTreeNode(150, null, null);
            BinaryTreeNode nodeRoot = new BinaryTreeNode(100, node2left, node2right);

            System.out.println(bt.isBalanced(nodeRoot, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }

        //three level--balanced
        {
            BinaryTreeNode node3_1 = new BinaryTreeNode(25, null, null);
            BinaryTreeNode node3_2 = new BinaryTreeNode(75, null, null);
            BinaryTreeNode node2left = new BinaryTreeNode(50, node3_1, node3_2);

            BinaryTreeNode node3_3 = new BinaryTreeNode(125, null, null);
            BinaryTreeNode node3_4 = new BinaryTreeNode(175, null, null);
            BinaryTreeNode node2right = new BinaryTreeNode(150, node3_3, node3_4);

            BinaryTreeNode nodeRoot = new BinaryTreeNode(100, node2left, node2right);

            System.out.println(bt.isBalanced(nodeRoot, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }

        //three level--not balanced
        {
            BinaryTreeNode node3_1 = new BinaryTreeNode(25, null, null);
            BinaryTreeNode node3_2 = new BinaryTreeNode(102, null, null);
            BinaryTreeNode node2left = new BinaryTreeNode(50, node3_1, node3_2);

            BinaryTreeNode node3_3 = new BinaryTreeNode(125, null, null);
            BinaryTreeNode node3_4 = new BinaryTreeNode(175, null, null);
            BinaryTreeNode node2right = new BinaryTreeNode(150, node3_3, node3_4);

            BinaryTreeNode nodeRoot = new BinaryTreeNode(100, node2left, node2right);

            System.out.println(bt.isBalanced(nodeRoot, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }

        //not balanced
        {
            BinaryTreeNode node2left = new BinaryTreeNode(50, null, null);
            BinaryTreeNode node2right = new BinaryTreeNode(90, null, null);
            BinaryTreeNode nodeRoot = new BinaryTreeNode(100, node2left, node2right);

            System.out.println(bt.isBalanced(nodeRoot, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }

        //not balanced
        {
            BinaryTreeNode node2left = new BinaryTreeNode(110, null, null);
            BinaryTreeNode node2right = new BinaryTreeNode(90, null, null);
            BinaryTreeNode nodeRoot = new BinaryTreeNode(100, node2left, node2right);

            System.out.println(bt.isBalanced(nodeRoot, Integer.MAX_VALUE, Integer.MIN_VALUE));
        }


    }
}
