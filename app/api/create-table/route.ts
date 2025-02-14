import { PrismaClient } from "@prisma/client";
import { NextResponse } from "next/server";

const prisma = new PrismaClient();

export async function POST(req: Request) {
  try {
    const { name, email, password, role } = await req.json();

    // Validação: Se a role não for ADMIN nem FUNCIONARIO, retorna erro
    if (role !== "ADMIN" && role !== "FUNCIONARIO") {
      return NextResponse.json({ error: "Função inválida" }, { status: 400 });
    }

    const user = await prisma.user.create({
      data: { name, email, password, role },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Erro ao criar usuário" }, { status: 500 });
  }
}

export async function GET() {
    const users = await prisma.user.findMany();
    return NextResponse.json(users);
}


export async function PUT(req: Request) {
    try {
      const { id, name, role } = await req.json();
  
      const updatedUser = await prisma.user.update({
        where: { id },
        data: { name, role },
      });
  
      return NextResponse.json(updatedUser);
    } catch (error) {
      return NextResponse.json({ error: "Erro ao atualizar usuário" }, { status: 500 });
    }
  }
  
export async function DELETE(req: Request) {
    try {
      const { id } = await req.json();
  
      await prisma.user.delete({ where: { id } });
  
      return NextResponse.json({ message: "Usuário deletado" });
    } catch (error) {
      return NextResponse.json({ error: "Erro ao deletar usuário" }, { status: 500 });
    }
  }
  