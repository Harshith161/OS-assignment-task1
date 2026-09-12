package ProdCons;

public class ProducerConsumer {

    static int data;
    static boolean available = false;

    static synchronized void produce(int value) {
        try {
            while (available) {
                ProducerConsumer.class.wait();
            }

            data = value;
            System.out.println("Producer produced: " + value);
            available = true;
            ProducerConsumer.class.notify();

        } catch (Exception e) {
            System.out.println(e);
        }
    }

    static synchronized void consume() {
        try {
            while (!available) {
                ProducerConsumer.class.wait();
            }

            System.out.println("Consumer consumed: " + data);
            available = false;
            ProducerConsumer.class.notify();

        } catch (Exception e) {
            System.out.println(e);
        }
    }

    static class Producer extends Thread {
        public void run() {
            for (int i = 1; i <= 5; i++) {
                produce(i);

                try {
                    Thread.sleep(500);
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    static class Consumer extends Thread {
        public void run() {
            for (int i = 1; i <= 5; i++) {
                consume();

                try {
                    Thread.sleep(700);
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    public static void main(String[] args) {
        Producer p = new Producer();
        Consumer c = new Consumer();

        p.start();
        c.start();
    }
}
