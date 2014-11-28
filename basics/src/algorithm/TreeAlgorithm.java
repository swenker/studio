package algorithm;

/**
 * Created with IntelliJ IDEA.
 * User: samsung
 * Date: 14-11-20
 * Time: 上午11:45
 * To change this template use File | Settings | File Templates.
 */
public class TreeAlgorithm {

    static class BinaryTreeNode{
        String value;
        BinaryTreeNode left;
        BinaryTreeNode right;

        public BinaryTreeNode(String value, BinaryTreeNode left, BinaryTreeNode right) {
            this.value = value;
            this.left = left;
            this.right = right;
        }

    }

    static  class BinaryTree{
        BinaryTreeNode root;

        BinaryTree(BinaryTreeNode root) {
            this.root = root;
        }
    }

    public void traverse(){
        BinaryTreeNode root =new BinaryTreeNode("a",null,null);
        BinaryTree tree = new BinaryTree(root);
        root.left=new BinaryTreeNode("b",null,null);
        root.right=new BinaryTreeNode("c",null,null);

        root.left.left=new BinaryTreeNode("d",null,null);
        root.left.right=new BinaryTreeNode("e",null,null);
        root.right.left=new BinaryTreeNode("f",null,null);
        root.right.right=new BinaryTreeNode("g",null,null);

        preorder(root);
        System.out.println();
        postorder(root);
        System.out.println();
        inorder(root);
    }

    public void preorder(BinaryTreeNode root){
        if(root==null) return;
        System.out.print(root.value);
        preorder(root.left);
        preorder(root.right);
    }
    public void inorder(BinaryTreeNode root){
        if(root==null) return;
        inorder(root.left);
        System.out.print(root.value);
        inorder(root.right);
    }

    public void postorder(BinaryTreeNode root){
        if(root==null) return;
        postorder(root.left);
        postorder(root.right);
        System.out.print(root.value);
    }


    public static void main(String args[]){
        TreeAlgorithm ta = new TreeAlgorithm();
        ta.traverse();
    }

}
