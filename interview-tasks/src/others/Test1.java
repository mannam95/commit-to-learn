package others;

public class Test1 {
    public static void main(String[] args) {
        B b = new B();
        b.m();
        b.calIM();
        b.callSuperM();
        A a = new B();
        a.m();
        a.calIM();
        A a1 = new A();
        a1.calIM();
        a1.m();
    }
}


class A implements I1 {
    public void calIM() {
        m();
    }
}

class B extends A implements I2 {

    public void callSuperM() {
        super.m();
    }
}

interface I1 {
    default void m() {
        System.out.print("I1 ");
    }
}

interface I2 extends I1 {
    default void m() {
        System.out.print("I2 ");
    }
}
